import os
from typing import List, Dict, Optional

from PIL import Image, ImageDraw

from .grid import Cell


def generate_grid_image_with_images(grid, image_paths: Dict[str, str], path: Optional[List[Cell]] = None,
                                    output_filename: str = 'grid_map_visualization.png'):
    """
    Creates a 1000x1000 pixel image from a grid, replacing symbols with 10x10  images.
    Path is shown with orange circles.
    """
    cell_size = 10
    image_size = 1000

    # new blank image
    image = Image.new('RGB', (image_size, image_size), 'white')
    draw = ImageDraw.Draw(image)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    images_dir = os.path.join(project_root, 'images')

    loaded_images = {}
    for symbol, img_filename in image_paths.items():
        image_full_path = os.path.join(images_dir, img_filename)  # Moved assignment outside try block
        try:
            loaded_images[symbol] = Image.open(image_full_path).resize((cell_size, cell_size))
        except FileNotFoundError as e:
            print(
                f'Error: Image file not found for symbol "{symbol}" at "{image_full_path}":'
                f' {e}. This terrain type will use default gray.')
            loaded_images[symbol] = None  # Mark as missing or problematic
        except Exception as e:
            print(f'Error loading image for symbol "{symbol}" from "{image_full_path}": {e}. Using default gray.')
            loaded_images[symbol] = None

    # draw the grid cells
    for r in range(grid.height):
        for c in range(grid.width):
            cell = grid.get_cell(c, r)
            if cell:
                symbol = cell.environment_type.symbol
                x1 = c * cell_size
                y1 = r * cell_size

                if symbol in loaded_images and loaded_images[symbol] is not None:
                    image.paste(loaded_images[symbol], (x1, y1))
                else:
                    #  gray color if image is not found
                    if symbol not in image_paths:
                        print(
                            f'Warning: No image path provided for terrain symbol "{symbol}". Drawing default gray.')
                    draw.rectangle([x1, y1, x1 + cell_size, y1 + cell_size], fill=(128, 128, 128))  # Default gray
            else:
                print(f"Warning: Cell at ({c},{r}) is None. Drawing default gray.")
                draw.rectangle([c * cell_size, r * cell_size, (c + 1) * cell_size, (r + 1) * cell_size],
                               fill=(128, 128, 128))

    # draw the path
    if path:
        path_color = (255, 165, 0)  # Orange for the path
        path_dot_radius = 3  # Size of the orange circle

        for cell in path:
            if (grid.start_node and cell.coords == grid.start_node.coords) or \
                    (grid.end_node and cell.coords == grid.end_node.coords):
                continue

            x_center = cell.x * cell_size + cell_size // 2
            y_center = cell.y * cell_size + cell_size // 2
            # draw an orange circle at the path's cell
            draw.ellipse([x_center - path_dot_radius, y_center - path_dot_radius,
                          x_center + path_dot_radius, y_center + path_dot_radius],
                         fill=path_color)

    start_end_marker_size = 8
    start_color = (0, 255, 0)
    end_color = (255, 0, 0)

    if grid.start_node:
        start_x_center = grid.start_node.x * cell_size + cell_size // 2
        start_y_center = grid.start_node.y * cell_size + cell_size // 2
        draw.ellipse([start_x_center - start_end_marker_size, start_y_center - start_end_marker_size,
                      start_x_center + start_end_marker_size, start_y_center + start_end_marker_size],
                     fill=start_color, outline=(0, 0, 0), width=1)

    if grid.end_node:
        end_x_center = grid.end_node.x * cell_size + cell_size // 2
        end_y_center = grid.end_node.y * cell_size + cell_size // 2
        draw.ellipse([end_x_center - start_end_marker_size, end_y_center - start_end_marker_size,
                      end_x_center + start_end_marker_size, end_y_center + start_end_marker_size],
                     fill=end_color, outline=(0, 0, 0), width=1)

    # final image
    output_full_path = os.path.join(project_root, output_filename)
    image.save(output_full_path)
    print(f'Generated visualization: {output_full_path}')
