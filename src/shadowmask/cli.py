"""
Command-line interface for ShadowMask
"""

import argparse
import os
import sys
from typing import List
from .core import ShadowMask
from .banner import print_banner, ABOUT

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description=ABOUT,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "input",
        help="Input image file or directory"
    )
    
    parser.add_argument(
        "-o", "--output",
        help="Output file or directory (default: input_protected)",
        default=None
    )
    
    parser.add_argument(
        "-m", "--methods",
        nargs="+",
        choices=["alpha_layer", "adversarial", "encoder", "diffusion", "all"],
        default=["alpha_layer", "adversarial"],
        help="Protection methods to apply"
    )
    
    parser.add_argument(
        "-i", "--intensity",
        type=float,
        default=0.5,
        help="Protection intensity (0.0 to 1.0)"
    )
    
    parser.add_argument(
        "-r", "--recursive",
        action="store_true",
        help="Process directories recursively"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show detailed progress information"
    )
    
    return parser.parse_args()

def process_path(
    input_path: str,
    output_path: str,
    methods: List[str],
    intensity: float,
    verbose: bool = False
) -> str:
    """Process a single file"""
    try:
        shadowmask = ShadowMask()
        
        # Handle "all" methods
        if "all" in methods:
            methods = ["alpha_layer", "adversarial", "encoder", "diffusion"]
            
        if verbose:
            print(f"Processing: {input_path}")
            print(f"Methods: {', '.join(methods)}")
            print(f"Intensity: {intensity}")
            
        return shadowmask.protect_image(
            input_path,
            methods=methods,
            output_path=output_path,
            intensity=intensity
        )
    except Exception as e:
        raise RuntimeError(f"Failed to process {input_path}: {str(e)}")

def main():
    """Main entry point"""
    print_banner()
    args = parse_args()
    
    # Validate intensity
    if not 0 <= args.intensity <= 1:
        print("Error: Intensity must be between 0.0 and 1.0", file=sys.stderr)
        return 1
    
    # Handle single file
    if os.path.isfile(args.input):
        if args.output is None:
            base, ext = os.path.splitext(args.input)
            args.output = f"{base}_protected.png"  # Always save as PNG
            
        try:
            process_path(args.input, args.output, args.methods, args.intensity, args.verbose)
            print(f"Protected image saved to: {args.output}")
        except Exception as e:
            print(f"Error: {str(e)}", file=sys.stderr)
            return 1
            
    # Handle directory
    elif os.path.isdir(args.input):
        if args.output is None:
            args.output = f"{args.input}_protected"
            
        os.makedirs(args.output, exist_ok=True)
        processed = 0
        failed = 0
        
        for root, _, files in os.walk(args.input):
            if not args.recursive and root != args.input:
                continue
                
            rel_path = os.path.relpath(root, args.input)
            out_dir = os.path.join(args.output, rel_path)
            os.makedirs(out_dir, exist_ok=True)
            
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                    in_path = os.path.join(root, file)
                    out_path = os.path.join(out_dir, f"protected_{os.path.splitext(file)[0]}.png")
                    
                    try:
                        process_path(in_path, out_path, args.methods, args.intensity, args.verbose)
                        processed += 1
                        if args.verbose:
                            print(f"Protected: {in_path} -> {out_path}")
                    except Exception as e:
                        failed += 1
                        print(f"Error processing {in_path}: {str(e)}", file=sys.stderr)
                        continue
                        
        print(f"\nProcessing complete:")
        print(f"Successfully processed: {processed} images")
        if failed > 0:
            print(f"Failed to process: {failed} images", file=sys.stderr)
            return 1
    else:
        print(f"Error: {args.input} does not exist", file=sys.stderr)
        return 1
        
    return 0

if __name__ == "__main__":
    exit(main())
