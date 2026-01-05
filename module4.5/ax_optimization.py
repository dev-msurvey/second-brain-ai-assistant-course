#!/usr/bin/env python3
"""
Meta Ax Hyperparameter Optimization for AI Director LoRA Training

Uses Bayesian optimization to find the best hyperparameters for fine-tuning.
Optimizes: LoRA rank, alpha, learning rate, batch size

Module 4.5: Hyperparameter Optimization
AI Director v3.4
"""

import json
import yaml
import torch
import pandas as pd
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import argparse

from ax.service.ax_client import AxClient
from ax.service.utils.instantiation import ObjectiveProperties
from ax.plot.trace import optimization_trace_single_method
from ax.plot.contour import plot_contour
from loguru import logger

# Import training function from Module 4
import sys
module4_path = str(Path(__file__).parent.parent / "module4" / "scripts")
if module4_path not in sys.path:
    sys.path.insert(0, module4_path)

try:
    from finetune_lora import AIDirectorFineTuner, FineTuningConfig
except ImportError:
    # For Colab: try different path
    sys.path.insert(0, "../module4/scripts")
    from finetune_lora import AIDirectorFineTuner, FineTuningConfig


class HyperparameterOptimizer:
    """
    Bayesian optimization for LoRA hyperparameters using Meta Ax
    """
    
    def __init__(
        self,
        config_path: str = "configs/optimization_config.yaml",
        output_dir: str = "configs/",
        verbose: bool = True
    ):
        """
        Initialize optimizer
        
        Args:
            config_path: Path to optimization config YAML
            output_dir: Directory to save results
            verbose: Print progress messages
        """
        self.config_path = Path(config_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.verbose = verbose
        
        # Load config
        with open(self.config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        # Setup logging
        logger.add(
            self.output_dir.parent / "logs" / f"optimization_{datetime.now():%Y%m%d_%H%M%S}.log",
            rotation="500 MB",
            level="INFO"
        )
        
        self.ax_client = None
        self.trial_results = []
        
    def setup_ax_client(self):
        """Setup Ax client with search space"""
        if self.verbose:
            print("=" * 70)
            print("🎯 SETTING UP META AX OPTIMIZATION")
            print("=" * 70)
            print()
        
        self.ax_client = AxClient()
        
        # Define search space from config
        parameters = []
        for param_name, param_config in self.config['search_space'].items():
            param_type = param_config['type']
            
            if param_type == 'choice':
                parameters.append({
                    "name": param_name,
                    "type": "choice",
                    "values": param_config['values'],
                    "value_type": "int" if isinstance(param_config['values'][0], int) else "float"
                })
            elif param_type == 'range':
                parameters.append({
                    "name": param_name,
                    "type": "range",
                    "bounds": param_config['bounds'],
                    "value_type": "float",
                    "log_scale": param_config.get('log_scale', False)
                })
        
        # Create experiment
        self.ax_client.create_experiment(
            name="ai_director_lora_optimization",
            parameters=parameters,
            objectives={
                "eval_loss": ObjectiveProperties(minimize=True)
            },
        )
        
        if self.verbose:
            print("✅ Ax Client created with search space:")
            print(json.dumps(self.config['search_space'], indent=2))
            print()
    
    def evaluate_hyperparameters(
        self,
        trial_params: Dict[str, Any]
    ) -> float:
        """
        Train model with given hyperparameters and return validation loss
        
        Args:
            trial_params: Hyperparameters from Ax
            
        Returns:
            Validation loss (lower is better)
        """
        if self.verbose:
            print(f"\n{'='*70}")
            print(f"🔬 EVALUATING TRIAL")
            print(f"{'='*70}")
            print(f"Parameters: {trial_params}")
            print()
        
        try:
            # Create training config with trial hyperparameters
            train_config = FineTuningConfig(
                # Hyperparameters from Ax
                lora_r=trial_params['lora_rank'],
                lora_alpha=trial_params['lora_alpha'],
                learning_rate=trial_params['learning_rate'],
                per_device_train_batch_size=trial_params['batch_size'],
                
                # Fixed parameters from config
                num_train_epochs=self.config['fixed_params']['num_train_epochs'],
                warmup_ratio=self.config['fixed_params']['warmup_ratio'],
                gradient_accumulation_steps=self.config['fixed_params']['gradient_accumulation_steps'],
                max_seq_length=2048,
                
                # Output (temporary for trial)
                output_dir=f"checkpoints/trial_{datetime.now():%Y%m%d_%H%M%S}",
                logs_dir="logs",
                
                # Dataset
                dataset_path=self.config['dataset']['path']
            )
            
            # Train model
            trainer = AIDirectorFineTuner(train_config)
            trainer.check_gpu()
            trainer.load_tokenizer()
            trainer.load_model()
            trainer.apply_lora()
            trainer.load_dataset()
            
            # Run training (1 epoch for fast evaluation)
            result = trainer.train()
            
            # Get validation loss
            eval_loss = result['eval_loss']
            
            if self.verbose:
                print(f"\n✅ Trial completed!")
                print(f"   Eval Loss: {eval_loss:.4f}")
                print()
            
            logger.info(f"Trial params: {trial_params} → Loss: {eval_loss:.4f}")
            
            # Clean up checkpoint to save space
            import shutil
            if Path(train_config.output_dir).exists():
                shutil.rmtree(train_config.output_dir)
            
            return eval_loss
            
        except Exception as e:
            logger.error(f"Trial failed: {e}")
            if self.verbose:
                print(f"❌ Trial failed: {e}")
            # Return high loss for failed trials
            return 1.0
    
    def run_optimization(
        self,
        num_trials: int = None,
        save_every: int = 5
    ) -> Dict[str, Any]:
        """
        Run Bayesian optimization
        
        Args:
            num_trials: Number of trials to run (default from config)
            save_every: Save checkpoint every N trials
            
        Returns:
            Optimization results with best parameters
        """
        if num_trials is None:
            num_trials = self.config['optimization']['num_trials']
        
        # Setup Ax
        self.setup_ax_client()
        
        if self.verbose:
            print("=" * 70)
            print(f"🚀 STARTING OPTIMIZATION ({num_trials} trials)")
            print("=" * 70)
            print(f"Baseline: {self.config['baseline']}")
            print(f"Target: Beat loss of {self.config['baseline']['loss']:.4f}")
            print()
        
        # Run optimization loop
        for trial_idx in range(num_trials):
            if self.verbose:
                print(f"\n{'#'*70}")
                print(f"# TRIAL {trial_idx + 1}/{num_trials}")
                print(f"{'#'*70}")
            
            # Get next trial parameters from Ax
            parameters, trial_index = self.ax_client.get_next_trial()
            
            # Evaluate
            eval_loss = self.evaluate_hyperparameters(parameters)
            
            # Report to Ax
            self.ax_client.complete_trial(
                trial_index=trial_index,
                raw_data=eval_loss
            )
            
            # Save trial result
            self.trial_results.append({
                'trial': trial_idx + 1,
                'parameters': parameters,
                'eval_loss': eval_loss,
                'timestamp': datetime.now().isoformat()
            })
            
            # Save checkpoint
            if (trial_idx + 1) % save_every == 0:
                self._save_checkpoint()
        
        # Get best parameters
        best_parameters, values = self.ax_client.get_best_parameters()
        
        if self.verbose:
            print("\n" + "=" * 70)
            print("🏆 OPTIMIZATION COMPLETE!")
            print("=" * 70)
            print(f"Best Parameters: {best_parameters}")
            print(f"Best Loss: {values[0]['eval_loss']:.4f}")
            print(f"Baseline Loss: {self.config['baseline']['loss']:.4f}")
            improvement = (self.config['baseline']['loss'] - values[0]['eval_loss']) / self.config['baseline']['loss'] * 100
            print(f"Improvement: {improvement:+.1f}%")
            print("=" * 70)
        
        # Save results
        results = {
            'best_parameters': best_parameters,
            'best_loss': values[0]['eval_loss'],
            'baseline_loss': self.config['baseline']['loss'],
            'improvement_percent': improvement,
            'num_trials': num_trials,
            'all_trials': self.trial_results,
            'timestamp': datetime.now().isoformat()
        }
        
        self._save_results(results)
        self._generate_visualizations()
        
        return results
    
    def _save_checkpoint(self):
        """Save optimization checkpoint"""
        checkpoint_path = self.output_dir / "optimization_checkpoint.json"
        checkpoint = {
            'trial_results': self.trial_results,
            'timestamp': datetime.now().isoformat()
        }
        with open(checkpoint_path, 'w') as f:
            json.dump(checkpoint, f, indent=2)
        
        if self.verbose:
            print(f"💾 Checkpoint saved: {checkpoint_path}")
    
    def _save_results(self, results: Dict[str, Any]):
        """Save final optimization results"""
        # Save JSON
        results_path = self.output_dir / "optimization_results.json"
        with open(results_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        # Save best config as YAML
        best_config_path = self.output_dir / "best_config.yaml"
        best_config = {
            'model': self.config['fixed_params']['model_name'],
            'lora_rank': results['best_parameters']['lora_rank'],
            'lora_alpha': results['best_parameters']['lora_alpha'],
            'learning_rate': results['best_parameters']['learning_rate'],
            'batch_size': results['best_parameters']['batch_size'],
            'best_loss': results['best_loss'],
            'improvement': f"{results['improvement_percent']:.1f}%",
            'optimized_at': results['timestamp']
        }
        with open(best_config_path, 'w') as f:
            yaml.dump(best_config, f, default_flow_style=False)
        
        # Save trial history as CSV
        df = pd.DataFrame(self.trial_results)
        csv_path = self.output_dir / "trial_history.csv"
        df.to_csv(csv_path, index=False)
        
        if self.verbose:
            print(f"\n💾 Results saved:")
            print(f"   - {results_path}")
            print(f"   - {best_config_path}")
            print(f"   - {csv_path}")
    
    def _generate_visualizations(self):
        """Generate optimization plots"""
        if self.verbose:
            print("\n📊 Generating visualizations...")
        
        try:
            # Optimization trace
            fig = optimization_trace_single_method(
                y=[[r['eval_loss']] for r in self.trial_results],
                title="Optimization Trace",
                ylabel="Validation Loss"
            )
            trace_path = self.output_dir / "optimization_trace.html"
            fig.write_html(str(trace_path))
            
            if self.verbose:
                print(f"   ✅ Trace plot: {trace_path}")
                
        except Exception as e:
            logger.warning(f"Could not generate visualizations: {e}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Optimize LoRA hyperparameters with Meta Ax")
    parser.add_argument(
        "--config",
        type=str,
        default="configs/optimization_config.yaml",
        help="Path to optimization config"
    )
    parser.add_argument(
        "--trials",
        type=int,
        default=None,
        help="Number of trials (overrides config)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="configs/",
        help="Output directory"
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Reduce output verbosity"
    )
    
    args = parser.parse_args()
    
    # Run optimization
    optimizer = HyperparameterOptimizer(
        config_path=args.config,
        output_dir=args.output,
        verbose=not args.quiet
    )
    
    results = optimizer.run_optimization(num_trials=args.trials)
    
    print("\n🎉 Optimization complete!")
    print(f"Best config saved to: {args.output}/best_config.yaml")


if __name__ == "__main__":
    main()
