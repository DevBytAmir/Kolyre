"""A demo utility for the Kolyre terminal styling library.

This script showcases the full range of Kolyre's capabilities,
including ANSI 16-color mode, extended 256-color palettes, customizable
text styles, and high-fidelity truecolor (RGB) gradients.
"""

import argparse
import importlib.metadata
import shutil
import sys

from .core import Kolyre


class Demo:
    """Provides static methods to generate and display Kolyre styling demos."""

    DEFAULT_RGB_STEP: int = 51
    DEFAULT_FOREGROUND_BLOCK: str = "ABC"
    DEFAULT_BACKGROUND_BLOCK: str = "ABC"
    FALLBACK_TERMINAL_WIDTH: int = 80
    GRID_CELL_PADDING: int = 2

    @staticmethod
    def _get_constants(
        const_class: type, exclude_keywords: list[str] | None = None
    ) -> list[tuple[str, str]]:
        """Retrieve public, uppercase constants from a class.

        Args:
            const_class: The class to inspect .
            exclude_keywords: A list of substrings to filter out constants.

        Returns:
            A list of (name, value) tuples for each matching constant.
        """
        if exclude_keywords is None:
            exclude_keywords = []
        return [
            (name, getattr(const_class, name))
            for name in dir(const_class)
            if not name.startswith("_")
            and name.isupper()
            and not any(kw in name for kw in exclude_keywords)
        ]

    COLOR_CATEGORIES: dict[str, list[tuple[str, str]]] = {
        "16-Color Foreground Palette": _get_constants(Kolyre.Foreground),
        "16-Color Background Palette": _get_constants(Kolyre.Background),
    }

    STYLE_CATEGORIES: dict[str, list[tuple[str, str]]] = {
        "Text Styles": _get_constants(
            Kolyre.Style,
            exclude_keywords=[
                "RESET",
                "RESET_BOLD_DIM",
                "RESET_ITALIC",
                "RESET_UNDERLINE",
                "RESET_REVERSED",
                "RESET_HIDDEN",
                "RESET_STRIKETHROUGH",
                "RESET_OVERLINE",
                "RESET_FOREGROUND",
                "RESET_BACKGROUND",
            ],
        )
    }

    @staticmethod
    def _get_terminal_width() -> int:
        """Retrieve the current terminal width safely.

        Returns:
            int: Width of the terminal in columns.
        """
        try:
            return shutil.get_terminal_size().columns
        except OSError:
            return Demo.FALLBACK_TERMINAL_WIDTH

    @staticmethod
    def _calculate_items_per_row(maximum_item_length: int, padding: int = 2) -> int:
        """Calculate the maximum number of items that fit in a terminal row.

        Args:
            maximum_item_length: The width of each item in characters.
            padding: Number of spaces between items. Defaults to 2.

        Returns:
            int: Number of items per row.
        """
        terminal_width = Demo._get_terminal_width()
        return max(terminal_width // (maximum_item_length + padding), 1)

    @staticmethod
    def render_header(section_title: str) -> None:
        """Render a formatted, colorized section header.

        Args:
            section_title: The title text of the section.
        """
        header_text = f" {section_title} "
        width = Demo._get_terminal_width()
        print(
            f"\n{Kolyre.colorize(header_text.center(width, '='),
            Kolyre.Style.BOLD, Kolyre.Foreground.CYAN)}\n"
        )

    @staticmethod
    def render_category_grid(
        category_mapping: dict[str, list[tuple[str, str]]],
    ) -> None:
        """Render a grid display for categories of text styles or colors.

        Args:
            category_mapping: Mapping of category names to (display_name, ANSI_code)
                pairs.
        """
        for category_name, category_items in category_mapping.items():
            if not category_items:
                continue

            maximum_length = (
                max(len(item_name) for item_name, _ in category_items)
                + Demo.GRID_CELL_PADDING
            )
            items_per_row = Demo._calculate_items_per_row(maximum_length)
            Demo.render_header(category_name)

            for index in range(0, len(category_items), items_per_row):
                row_text = " ".join(
                    f"{color_code}{item_name:<{maximum_length}}{Kolyre.Style.RESET}"
                    for item_name, color_code in category_items[
                        index : index + items_per_row
                    ]
                )
                print(row_text)

    @staticmethod
    def render_text_styles() -> None:
        """Render all available text styles."""
        Demo.render_category_grid(Demo.STYLE_CATEGORIES)

    @staticmethod
    def render_16_palette() -> None:
        """Render the 16-Color ANSI foreground and background color palette."""
        Demo.render_category_grid(Demo.COLOR_CATEGORIES)

    @staticmethod
    def render_256_palette(is_foreground: bool = True) -> None:
        """Render the full 256-color ANSI palette.

        Args:
            is_foreground: True for foreground, False for background.
        """
        title = f"256-Color Palette ({'Foreground' if is_foreground else 'Background'})"
        Demo.render_header(title)

        items_per_row = Demo._calculate_items_per_row(4, 1)
        for color_index in range(256):
            color_label = f"{color_index:>3}"
            color_code = (
                Kolyre.foreground_256(color_index)
                if is_foreground
                else Kolyre.background_256(color_index)
            )
            print(f"{color_code}{color_label}{Kolyre.Style.RESET}", end=" ")
            if (color_index + 1) % items_per_row == 0:
                print()
        if 256 % items_per_row != 0:
            print()

    @staticmethod
    def render_rgb_gradient(
        is_foreground: bool, rgb_step: int, display_block: str
    ) -> None:
        """Render a truecolor RGB gradient demo.

        Args:
            is_foreground: True for text foreground, False for background.
            rgb_step: Step size for each RGB component.
            display_block: Character or string to display in the gradient.
        """
        title = (
            f"Truecolor RGB Gradient "
            f"({'Foreground' if is_foreground else 'Background'})"
        )
        Demo.render_header(title)

        items_per_row = Demo._calculate_items_per_row(len(display_block) + 1)
        count = 0

        for red_value in range(0, 256, rgb_step):
            for green_value in range(0, 256, rgb_step):
                for blue_value in range(0, 256, rgb_step):
                    color_code = (
                        Kolyre.foreground_rgb(red_value, green_value, blue_value)
                        if is_foreground
                        else Kolyre.background_rgb(red_value, green_value, blue_value)
                    )
                    print(f"{color_code}{display_block}{Kolyre.Style.RESET}", end=" ")
                    count += 1
                    if count % items_per_row == 0:
                        print()
        if count % items_per_row != 0:
            print()

    @staticmethod
    def run(parsed_arguments: argparse.Namespace) -> None:
        """Execute the appropriate demo based on parsed CLI arguments.

        Args:
            parsed_arguments (argparse.Namespace): Parsed command-line arguments.
        """
        if parsed_arguments.styles:
            Demo.render_text_styles()

        if parsed_arguments.palette16:
            Demo.render_16_palette()

        if parsed_arguments.palette256:
            Demo.render_256_palette(is_foreground=True)
            Demo.render_256_palette(is_foreground=False)

        if parsed_arguments.rgb:
            foreground_block = (
                parsed_arguments.rgb_block_fg or Demo.DEFAULT_FOREGROUND_BLOCK
            )
            background_block = (
                parsed_arguments.rgb_block_bg or Demo.DEFAULT_BACKGROUND_BLOCK
            )
            rgb_step = parsed_arguments.rgb_step
            Demo.render_rgb_gradient(
                is_foreground=True, rgb_step=rgb_step, display_block=foreground_block
            )
            Demo.render_rgb_gradient(
                is_foreground=False, rgb_step=rgb_step, display_block=background_block
            )


def show_version(parsed_arguments: argparse.Namespace, ansi_supported: bool) -> None:
    """
    Display the Kolyre package version and exit the program.

    Args:
        parsed_arguments (argparse.Namespace): Parsed command-line arguments.
        ansi_supported (bool): Indicates whether the terminal supports ANSI
            escape sequences.
    """
    try:
        version = importlib.metadata.version("kolyre")
        message = f"Kolyre {version}"
        styled = Kolyre.colorize(
            message,
            Kolyre.Style.BOLD,
            Kolyre.Foreground.BRIGHT_GREEN
        )
        print(styled if ansi_supported or parsed_arguments.force else message)
    except importlib.metadata.PackageNotFoundError:
        print("Error: Kolyre package metadata not found. Is it installed?")
    sys.exit(0)


def validate_rgb_flags(
    parsed_arguments: argparse.Namespace, ansi_supported: bool
) -> None:
    """
    Validate that RGB-related CLI options are only used when '--rgb' is enabled.

    Args:
        parsed_arguments (argparse.Namespace): Parsed command-line arguments.
        ansi_supported (bool): Indicates whether the terminal supports ANSI
            escape sequences.
    """
    rgb_flags_used = [
        parsed_arguments.rgb_step != Demo.DEFAULT_RGB_STEP,
        parsed_arguments.rgb_block_fg is not None,
        parsed_arguments.rgb_block_bg is not None,
    ]
    if not parsed_arguments.rgb and any(rgb_flags_used):
        rgb_flag_names = ["--rgb-step", "--rgb-block-fg", "--rgb-block-bg"]
        flags_used = [
            name for name, used in zip(rgb_flag_names, rgb_flags_used) if used
        ]

        error_msg = (
            "Error: RGB options specified without '--rgb' enabled.\n"
            f"These options require '--rgb': {', '.join(flags_used)}"
        )
        print(
            Kolyre.colorize(error_msg, Kolyre.Style.BOLD, Kolyre.Foreground.RED)
            if ansi_supported
            else error_msg
        )
        sys.exit(1)


def main() -> None:
    """Entry point for the Kolyre demo utility.

    Parses command-line arguments, validates ANSI support, and runs the
    requested demos.
    """
    parser = argparse.ArgumentParser(
        description="Demo utility for the Kolyre terminal styling library.",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    demo_options = parser.add_argument_group("Demo Options")
    demo_options.add_argument(
        "-a", "--all", action="store_true", help="Run all available demos."
    )
    demo_options.add_argument(
        "-s", "--styles", action="store_true", help="Display all available text styles."
    )
    demo_options.add_argument(
        "-p16",
        "--palette16",
        action="store_true",
        help="Display the standard 16-color ANSI palette.",
    )
    demo_options.add_argument(
        "-p256",
        "--palette256",
        action="store_true",
        help="Display the extended 256-color ANSI palette.",
    )
    demo_options.add_argument(
        "-r",
        "--rgb",
        action="store_true",
        help="Display the truecolor (RGB) gradient demo.",
    )

    rgb_options = parser.add_argument_group("RGB Gradient Options")
    rgb_options.add_argument(
        "-rs",
        "--rgb-step",
        type=int,
        default=Demo.DEFAULT_RGB_STEP,
        metavar="N",
        help=f"Step size for RGB components (default: {Demo.DEFAULT_RGB_STEP}).",
    )
    rgb_options.add_argument(
        "-rbf",
        "--rgb-block-fg",
        type=str,
        metavar="BLOCK",
        help=f"Text block for the foreground RGB gradient "
        f"(default: '{Demo.DEFAULT_FOREGROUND_BLOCK}').",
    )
    rgb_options.add_argument(
        "-rbb",
        "--rgb-block-bg",
        type=str,
        metavar="BLOCK",
        help=f"Text block for the background RGB gradient "
        f"(default: '{Demo.DEFAULT_BACKGROUND_BLOCK}').",
    )

    general_options = parser.add_argument_group("General Options")
    general_options.add_argument(
        "-V",
        "--version",
        action="store_true",
        help="Show the Kolyre package version and exit.",
    )
    general_options.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="Force execution even if ANSI support is unavailable.",
    )

    args = parser.parse_args()
    ansi_supported = Kolyre.enable_ansi_support()

    if args.force:
        Kolyre.FORCE_COLOR = True
        ansi_supported = True

    if args.all:
        args.palette16 = args.palette256 = args.styles = args.rgb = True

    if args.version:
        show_version(args, ansi_supported)

    validate_rgb_flags(args, ansi_supported)

    if not any((args.palette16, args.palette256, args.styles, args.rgb)):
        parser.print_help(sys.stderr)
        sys.exit(0)

    if args.rgb and not 1 <= args.rgb_step <= 255:
        error_msg = "Invalid --rgb-step value. Must be between 1 and 255."
        print(
            Kolyre.colorize(error_msg, Kolyre.Style.BOLD, Kolyre.Foreground.RED)
            if ansi_supported
            else error_msg
        )
        sys.exit(1)

    if ansi_supported:
        print(
            Kolyre.colorize(
                "ANSI terminal support enabled.",
                Kolyre.Style.BOLD,
                Kolyre.Foreground.BRIGHT_GREEN,
            )
        )
    elif args.force:
        print(
            Kolyre.colorize(
                "Continuing with --force.",
                Kolyre.Style.BOLD,
                Kolyre.Foreground.BRIGHT_YELLOW,
            )
        )
    else:
        print(
            "Failed to enable ANSI support.\n"
            "Ensure your terminal supports ANSI escape sequences.\n"
            "To bypass this check, use the '--force' flag."
        )
        sys.exit(1)

    Demo.run(args)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nDemo interrupted by user.")
        # pylint: disable=W0718
    except Exception as e:
        print(f"\nUnexpected error: {e}")
