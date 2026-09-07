"""
Modern, polished Command-Line Interface for GeoMind.
Supports interactive multi-turn chats, slash commands, model training, session history, and one-shot execution.
"""
import sys
import os
import argparse
from typing import Optional
from geomind.core.agent import GeoMind
from geomind.core.session import Session
from geomind.knowledge.geography import COUNTRIES_DATA, WORLD_CITIES
from geomind.knowledge.history import HISTORICAL_EVENTS, HISTORICAL_FIGURES
from geomind.knowledge.social_studies import SOCIAL_STUDIES_CONCEPTS
from geomind.models.dataset import GeoMindDataset
from geomind import __version__

# Check for Rich library
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.markdown import Markdown
    from rich.table import Table
    from rich.text import Text
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeRemainingColumn
    HAS_RICH = True
    console = Console()
except ImportError:
    HAS_RICH = False
    console = None


BANNER_TEXT = rf"""
   ____           __  __ _           _ 
  / ___| ___  ___|  \/  (_)_ __   __| |
 | |  _ / _ \/ _ \ |\/| | | '_ \ / _` |
 | |_| |  __/ (_) | |  | | | | | | (_| |
  \____|\___|\___/|_|  |_|_|_| |_|\__,_|
  Geography • History • Social Studies AI
  GeoMind-1 Foundation Model | v{__version__}
"""


def print_banner():
    if HAS_RICH:
        panel = Panel(
            Text(BANNER_TEXT.strip(), style="bold cyan"),
            title="[bold green]GeoMind AI CLI[/bold green]",
            subtitle="[dim]Powered by GeoMind-1 standalone neural model & symbolic reasoning[/dim]",
            border_style="cyan"
        )
        console.print(panel)
    else:
        print("\033[96m" + BANNER_TEXT + "\033[0m")
        print("-" * 60)


def print_help():
    if HAS_RICH:
        table = Table(title="🧭 GeoMind Commands & Features", border_style="cyan", show_header=True)
        table.add_column("Command / Action", style="bold yellow", width=24)
        table.add_column("Description", style="white")

        table.add_row("/help", "Display this interactive help menu")
        table.add_row("/model", "View GeoMind-1 model architecture & parameters")
        table.add_row("/train [epochs]", "Train or fine-tune the neural model interactively")
        table.add_row("/history", "View conversation history for the current session")
        table.add_row("/clear", "Clear the terminal screen")
        table.add_row("/info", "Display system architecture and active provider info")
        table.add_row("/stats", "Show knowledge base coverage statistics")
        table.add_row("/export [file]", "Export session history to a file (.md or .json)")
        table.add_row("/distance <A> <B>", "Direct geodesic distance calculation shortcut")
        table.add_row("/compare <A> <B>", "Side-by-side comparative analysis shortcut")
        table.add_row("/exit, /quit", "Exit the interactive session")

        console.print(table)
        console.print("\n[bold cyan]💡 Sample Natural Language Questions:[/bold cyan]")
        console.print("  • [italic]'ditace between delhi & mumbi'[/italic] (handles typos, abbreviations)")
        console.print("  • [italic]'what is the capital of Japan'[/italic]")
        console.print("  • [italic]'causes and consequences of World War 1'[/italic]")
        console.print("  • [italic]'compare capitalism and socialism'[/italic]")
        console.print("  • [italic]'who was Napoleon Bonaparte'[/italic]")
        console.print("  • [italic]'define federalism'[/italic]")
        console.print("  • [italic]'bordering countries of Germany'[/italic]\n")
    else:
        print("""
🧭 GeoMind Commands:
  /help               Display this interactive help menu
  /model              View GeoMind-1 model architecture & parameters
  /train [epochs]     Train or fine-tune the neural model
  /history            View current conversation session history
  /clear              Clear the terminal screen
  /info               Display system architecture & active provider
  /stats              Show knowledge base statistics
  /export <file>      Export session history (.md or .json)
  /distance <A> <B>   Calculate geodesic distance between two places
  /compare <A> <B>    Compare two countries, cities, events, or concepts
  /exit, /quit        Exit GeoMind

💡 Sample Questions:
  - ditace between delhi & mumbi
  - what is the capital of Japan
  - causes and consequences of World War 1
  - compare capitalism and socialism
  - who was Napoleon Bonaparte
  - define federalism
""")


def print_model_info(agent: GeoMind):
    if not agent.model:
        print("Model information unavailable.")
        return
    info = agent.model.get_info()
    text = f"""
🧠 **GeoMind-1 Model Architecture**
- **Model Name**: `{info['model_name']}`
- **Type**: Standalone Foundation Neural Transformer
- **Total Parameters**: {info['total_parameters']:,} trainable parameters
- **Architecture**: {info['architecture']}
- **Hidden Dimension**: {info['hidden_dimension']}
- **Transformer Layers**: {info['layers']}
- **Attention Heads**: {info['attention_heads']}
- **Intermediate Dimension**: {info['intermediate_dimension']}
- **Vocabulary Size**: {info['vocabulary_size']} tokens
- **Trained Epochs**: {info['training_epochs_completed']}
- **Specialized Domains**: {', '.join(info['domains'])}
"""
    if HAS_RICH:
        console.print(Panel(Markdown(text), title="🧠 Model Specs", border_style="magenta"))
    else:
        print(text)


def print_info(agent: GeoMind):
    provider_name = agent.provider.name
    total_params = agent.model.total_parameters if agent.model else "N/A"
    info_text = f"""
**GeoMind Architecture & System Information**
- **Version**: {__version__}
- **Active Model**: `{provider_name}` ({total_params:,} parameters)
- **PyPI Package**: `geomind-ai`
- **Model Type**: Standalone Neural Transformer & Symbolic Grounding Engine
- **Knowledge Domains**: Geography, History, Social Studies, Geodesic Distance
- **NLP Capabilities**: Damerau-Levenshtein fuzzy matching, phonetic normalization, abbreviation expansion
- **External Dependencies**: Zero required (pure Python runtime)
"""
    if HAS_RICH:
        console.print(Panel(Markdown(info_text), title="⚙️ System Info", border_style="blue"))
    else:
        print(info_text)


def print_stats():
    stats_text = f"""
📊 **GeoMind Knowledge Base Coverage**
- **Standardized Countries**: {len(COUNTRIES_DATA)} countries with borders, capitals, currencies, demographics
- **Major World Metropolises**: {len(WORLD_CITIES)} cities with exact coordinates and populations
- **Major Historical Eras & Events**: {len(HISTORICAL_EVENTS)} comprehensive event chronicles
- **Prominent Historical Figures**: {len(HISTORICAL_FIGURES)} biographical profiles
- **Social Studies Concepts**: {len(SOCIAL_STUDIES_CONCEPTS)} civics, economics, and sociology definitions
- **Geodesic Engine**: WGS84 ellipsoid Haversine calculation with bearing & travel time approximations
"""
    if HAS_RICH:
        console.print(Panel(Markdown(stats_text), title="📊 Knowledge Base Stats", border_style="green"))
    else:
        print(stats_text)


def print_response(result, query: str):
    """Prints a QueryResult with styled formatting and interpreted query banner."""
    if result.interpreted_query and result.interpreted_query.lower() != query.strip().lower():
        interp_msg = f"💡 Interpreted as: \"{result.interpreted_query}\""
        if HAS_RICH:
            console.print(f"[dim cyan]{interp_msg}[/dim cyan]\n")
        else:
            print(f"\033[90m\033[36m{interp_msg}\033[0m\n")

    if HAS_RICH:
        console.print(Markdown(result.text))
        if result.sources:
            sources_str = ", ".join(result.sources)
            console.print(f"\n[dim italic]Sources: {sources_str}[/dim italic]")
        console.print()
    else:
        print(result.text)
        if result.sources:
            print(f"\nSources: {', '.join(result.sources)}")
        print()


def run_interactive_training(agent: GeoMind, epochs: int = 5):
    """Runs interactive model training with progress updates."""
    if not agent.model:
        print("Model training unavailable.")
        return

    if HAS_RICH:
        console.print(f"[bold green]Starting GeoMind-1 neural training ({epochs} epochs)...[/bold green]")
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeRemainingColumn(),
            console=console
        ) as progress:
            task = progress.add_task("[cyan]Training model weights...", total=epochs)

            def update_ui(current, total, loss):
                progress.update(task, completed=current, description=f"[cyan]Epoch {current}/{total} (Loss: {loss:.4f})")

            agent.train(epochs=epochs, progress_callback=update_ui, verbose=False)
        console.print(f"[bold green]✓ Training complete! {agent.model.total_parameters:,} parameters tuned.[/bold green]\n")
    else:
        print(f"Starting GeoMind-1 neural training ({epochs} epochs)...")
        agent.train(epochs=epochs, verbose=True)
        print("Training complete!\n")


def run_interactive(agent: GeoMind):
    """Starts the interactive CLI loop."""
    print_banner()
    session = Session()

    while True:
        try:
            if HAS_RICH:
                user_input = console.input("[bold green]geomind[/bold green] [bold cyan]>[/bold cyan] ").strip()
            else:
                user_input = input("geomind > ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting GeoMind. Goodbye!")
            break

        if not user_input:
            continue

        cmd = user_input.lower()

        # Handle commands
        if cmd in ("/exit", "/quit", "exit", "quit"):
            print("Goodbye! Thank you for using GeoMind.")
            break
        elif cmd == "/clear":
            os.system("clear" if os.name != "nt" else "cls")
            print_banner()
            continue
        elif cmd in ("/help", "help", "?"):
            print_help()
            continue
        elif cmd in ("/model", "model"):
            print_model_info(agent)
            continue
        elif cmd.startswith("/train"):
            parts = user_input.split(maxsplit=1)
            epochs = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 5
            run_interactive_training(agent, epochs)
            continue
        elif cmd in ("/info", "info", "/system"):
            print_info(agent)
            continue
        elif cmd in ("/stats", "stats"):
            print_stats()
            continue
        elif cmd in ("/history", "history"):
            if not session.history:
                if HAS_RICH:
                    console.print("[dim]No messages in current session.[/dim]\n")
                else:
                    print("No messages in current session.\n")
            else:
                if HAS_RICH:
                    table = Table(title="📜 Session History", border_style="cyan")
                    table.add_column("Turn", style="bold yellow", width=6)
                    table.add_column("Role", style="bold", width=12)
                    table.add_column("Snippet / Query", style="white")
                    for idx, m in enumerate(session.history, 1):
                        snippet = m.content.split("\n")[0][:80]
                        table.add_row(str(idx), m.role.upper(), snippet)
                    console.print(table)
                    console.print()
                else:
                    for idx, m in enumerate(session.history, 1):
                        print(f"[{idx}] {m.role.upper()}: {m.content.splitlines()[0][:80]}")
                    print()
            continue
        elif cmd.startswith("/export"):
            parts = user_input.split(maxsplit=1)
            filename = parts[1].strip() if len(parts) > 1 else "geomind_session.md"
            if filename.endswith(".json"):
                session.export_json(filename)
            else:
                session.export_markdown(filename)
            if HAS_RICH:
                console.print(f"[green]Session successfully exported to {filename}[/green]\n")
            else:
                print(f"Session successfully exported to {filename}\n")
            continue
        elif cmd.startswith("/distance"):
            parts = user_input.split(maxsplit=2)
            if len(parts) < 3:
                print("Usage: /distance <Origin> <Destination>")
                continue
            user_input = f"distance between {parts[1]} and {parts[2]}"
        elif cmd.startswith("/compare"):
            parts = user_input.split(maxsplit=2)
            if len(parts) < 3:
                print("Usage: /compare <Item1> <Item2>")
                continue
            user_input = f"compare {parts[1]} and {parts[2]}"

        # Process standard question
        try:
            context_list = [m.__dict__ for m in session.history]
            result = agent.ask(user_input, context=context_list)
            session.add_user_message(user_input, interpreted_query=result.interpreted_query)
            session.add_assistant_message(result)
            print_response(result, user_input)
        except Exception as e:
            if HAS_RICH:
                console.print(f"[bold red]Error:[/bold red] {e}\n")
            else:
                print(f"Error: {e}\n")


def main():
    """Main entry point for CLI and command-line scripts."""
    parser = argparse.ArgumentParser(
        prog="geomind",
        description="GeoMind: An intelligent AI for Geography, History, and Social Studies."
    )
    parser.add_argument(
        "query",
        nargs="*",
        help="One-shot natural language question (e.g., 'ditace between delhi & mumbi')"
    )
    parser.add_argument(
        "--version", "-v",
        action="version",
        version=f"GeoMind v{__version__}"
    )
    parser.add_argument(
        "--model-info",
        action="store_true",
        help="Display GeoMind-1 model architecture and parameter count"
    )
    parser.add_argument(
        "--train",
        action="store_true",
        help="Train or fine-tune GeoMind neural model weights"
    )
    parser.add_argument(
        "--epochs",
        type=int,
        default=5,
        help="Number of training epochs (default: 5)"
    )
    parser.add_argument(
        "--lr",
        type=float,
        default=0.02,
        help="Learning rate for model training (default: 0.02)"
    )
    parser.add_argument(
        "--dataset",
        metavar="FILE",
        help="Path to custom training dataset JSON file"
    )
    parser.add_argument(
        "--export",
        metavar="FILE",
        help="Export one-shot result to a Markdown or JSON file"
    )

    args = parser.parse_args()

    agent = GeoMind()

    if args.model_info:
        print_model_info(agent)
        return

    if args.train:
        ds = GeoMindDataset.load_json(args.dataset) if args.dataset else None
        agent.train(epochs=args.epochs, learning_rate=args.lr, dataset=ds, verbose=True)
        return

    # Check if input is piped through stdin
    if not sys.stdin.isatty() and not args.query:
        piped_input = sys.stdin.read().strip()
        if piped_input:
            result = agent.ask(piped_input)
            print_response(result, piped_input)
            return

    # Check for one-shot query from CLI arguments
    if args.query:
        full_query = " ".join(args.query)
        result = agent.ask(full_query)
        print_response(result, full_query)
        if args.export:
            session = Session()
            session.add_user_message(full_query, interpreted_query=result.interpreted_query)
            session.add_assistant_message(result)
            if args.export.endswith(".json"):
                session.export_json(args.export)
            else:
                session.export_markdown(args.export)
        return

    # Otherwise, enter interactive mode
    run_interactive(agent)


if __name__ == "__main__":
    main()
