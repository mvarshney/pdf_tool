import PyPDF2
import os
import typer
from typing import Optional


# Create the main CLI app
app = typer.Typer(help="PDF manipulation utilities")


def crop_pdf(pdf_filename: str, left_margin: float, top_margin: float, 
             right_margin: Optional[float] = None, bottom_margin: Optional[float] = None) -> None:
    """
    Crop PDF pages by removing margins from all four sides.
    
    Args:
        pdf_filename (str): Path to the input PDF file
        left_margin (float): Left margin to remove (in points)
        top_margin (float): Top margin to remove (in points)
        right_margin (float, optional): Right margin to remove. If None, uses left_margin value
        bottom_margin (float, optional): Bottom margin to remove. If None, uses top_margin value
    
    The cropped PDF will be saved with '_cropped' suffix in the filename.
    """
    # Set default values for optional parameters
    if right_margin is None:
        right_margin = left_margin
    if bottom_margin is None:
        bottom_margin = top_margin
    
    # Check if input file exists
    if not os.path.exists(pdf_filename):
        raise FileNotFoundError(f"PDF file '{pdf_filename}' not found")
    
    # Create output filename
    base_name, ext = os.path.splitext(pdf_filename)
    output_filename = f"{base_name}_cropped{ext}"
    
    try:
        # Open the PDF file
        with open(pdf_filename, 'rb') as input_file:
            pdf_reader = PyPDF2.PdfReader(input_file)
            pdf_writer = PyPDF2.PdfWriter()
            
            print(f"Processing {len(pdf_reader.pages)} pages...")
            
            # Process each page
            for page_num, page in enumerate(pdf_reader.pages):
                # Get the current page dimensions
                mediabox = page.mediabox
                current_width = float(mediabox.width)
                current_height = float(mediabox.height)
                
                print(f"Page {page_num + 1}: Original size {current_width}x{current_height} points")
                
                # Calculate new dimensions after cropping
                new_lower_left_x = float(mediabox.lower_left[0]) + left_margin
                new_lower_left_y = float(mediabox.lower_left[1]) + bottom_margin
                new_upper_right_x = float(mediabox.upper_right[0]) - right_margin
                new_upper_right_y = float(mediabox.upper_right[1]) - top_margin
                
                # Validate that the margins don't exceed the page dimensions
                if new_lower_left_x >= new_upper_right_x:
                    raise ValueError(f"Left margin ({left_margin}) + right margin ({right_margin}) exceed page width ({current_width})")
                if new_lower_left_y >= new_upper_right_y:
                    raise ValueError(f"Bottom margin ({bottom_margin}) + top margin ({top_margin}) exceed page height ({current_height})")
                
                # Crop the page by adjusting the mediabox
                page.mediabox.lower_left = [new_lower_left_x, new_lower_left_y]
                page.mediabox.upper_right = [new_upper_right_x, new_upper_right_y]
                
                new_width = new_upper_right_x - new_lower_left_x
                new_height = new_upper_right_y - new_lower_left_y
                print(f"Page {page_num + 1}: Cropped size {new_width}x{new_height} points")
                
                # Add the cropped page to the writer
                pdf_writer.add_page(page)
            
            # Write the cropped PDF to output file
            with open(output_filename, 'wb') as output_file:
                pdf_writer.write(output_file)
                
        print(f"Successfully cropped PDF saved as: {output_filename}")
        
    except Exception as e:
        print(f"Error processing PDF: {str(e)}")
        raise


@app.command()
def crop(
    filename: str = typer.Argument(..., help="Path to the PDF file to crop"),
    left: float = typer.Argument(..., help="Left margin to remove (in points)"),
    top: float = typer.Argument(..., help="Top margin to remove (in points)"),
    right: Optional[float] = typer.Argument(None, help="Right margin to remove (defaults to left margin)"),
    bottom: Optional[float] = typer.Argument(None, help="Bottom margin to remove (defaults to top margin)")
):
    """
    Crop PDF pages by removing margins from all four sides.
    
    Margins are specified in points (1/72 inch).
    If right margin is not specified, it defaults to left margin.
    If bottom margin is not specified, it defaults to top margin.
    
    Examples:
    
        pdf-tool document.pdf 36 36          # Remove 36pt from all sides
        
        pdf-tool document.pdf 20 30 25 35    # Different margin for each side
    """
    try:
        crop_pdf(filename, left, top, right, bottom)
        typer.echo(f"✅ Successfully cropped PDF: {filename}")
    except FileNotFoundError as e:
        typer.echo(f"❌ Error: {e}", err=True)
        raise typer.Exit(1)
    except ValueError as e:
        typer.echo(f"❌ Error: {e}", err=True)
        raise typer.Exit(1)
    except Exception as e:
        typer.echo(f"❌ Unexpected error: {e}", err=True)
        raise typer.Exit(1)


# Entry point for the application
if __name__ == "__main__":
    app()
