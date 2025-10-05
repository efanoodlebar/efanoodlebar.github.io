from PIL import Image
import argparse
import sys

def create_dish(bowl_path, noodle_path, topping_paths, output_path="final_dish.png"):
    """
    Layer images to create a final dish composition.
    
    Args:
        bowl_path: Path to bowl/broth image
        noodle_path: Path to noodles image
        topping_paths: List of 1-3 topping image paths
        output_path: Where to save the final image
    """
    # Canvas size
    canvas_size = (1024, 1024)
    
    # Create transparent canvas
    final_image = Image.new('RGBA', canvas_size, (255, 255, 255, 0))
    
    # Define sizes (as percentages of canvas)
    sizes = {
        'bowl': 0.80,      # 80% of canvas
        'noodle': 0.60,    # 60% of canvas
        'topping': 0.40    # 40% of canvas
    }
    
    def resize_and_center(img, scale):
        """Resize image to scale and return centered position"""
        new_size = int(canvas_size[0] * scale)
        img_resized = img.resize((new_size, new_size), Image.Resampling.LANCZOS)
        
        # Calculate center position
        x = (canvas_size[0] - new_size) // 2
        y = (canvas_size[1] - new_size) // 2
        
        return img_resized, (x, y)
    
    # Layer 1: Bowl with broth
    bowl = Image.open(bowl_path).convert('RGBA')
    bowl_resized, bowl_pos = resize_and_center(bowl, sizes['bowl'])
    final_image.paste(bowl_resized, bowl_pos, bowl_resized)
    
    # Layer 2: Noodles
    noodles = Image.open(noodle_path).convert('RGBA')
    noodles_resized, noodles_pos = resize_and_center(noodles, sizes['noodle'])
    final_image.paste(noodles_resized, noodles_pos, noodles_resized)
    
    # Layer 3+: Toppings (scattered slightly for visual interest)
    offsets = [
        (0, -30),      # Topping 1: slightly up
        (-40, 25),     # Topping 2: left and down
        (40, 25)       # Topping 3: right and down
    ]
    
    for i, topping_path in enumerate(topping_paths[:3]):  # Max 3 toppings
        topping = Image.open(topping_path).convert('RGBA')
        topping_resized, base_pos = resize_and_center(topping, sizes['topping'])
        
        # Apply offset for variety
        offset_x, offset_y = offsets[i] if i < len(offsets) else (0, 0)
        topping_pos = (base_pos[0] + offset_x, base_pos[1] + offset_y)
        
        final_image.paste(topping_resized, topping_pos, topping_resized)
    
    # Save final image
    final_image.save(output_path, 'PNG')
    print(f"✅ Dish created successfully: {output_path}")
    
    return output_path


def main():
    parser = argparse.ArgumentParser(
        description='Create a fusion noodle dish by layering images',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python create_dish.py broth-tomyum.png noodle-spaghetti.png topping-pancetta.png
  python create_dish.py broth-pho.png noodle-ramen.png topping-egg.png topping-scallions.png topping-basil.png
  python create_dish.py broth-marinara.png noodle-fettuccine.png topping-parmesan.png -o my_dish.png
        '''
    )
    
    parser.add_argument('bowl', help='Path to bowl/broth image')
    parser.add_argument('noodles', help='Path to noodles image')
    parser.add_argument('toppings', nargs='+', help='Path(s) to 1-3 topping images')
    parser.add_argument('-o', '--output', default='final_dish.png', 
                        help='Output filename (default: final_dish.png)')
    
    args = parser.parse_args()
    
    # Validate number of toppings
    if len(args.toppings) > 3:
        print(f"⚠️  Warning: Maximum 3 toppings supported. Using first 3 only.")
        args.toppings = args.toppings[:3]
    
    try:
        create_dish(args.bowl, args.noodles, args.toppings, args.output)
    except FileNotFoundError as e:
        print(f"❌ Error: Could not find file - {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()