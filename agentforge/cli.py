import sys
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.spinner import Spinner
from .main import run_agent

console = Console()

def main():
    if len(sys.argv) < 2:
        console.print("[bold red]Error:[/bold red] Please provide a task description.")
        console.print("Usage: python -m agentforge.cli \"task description\"")
        sys.exit(1)

    user_task = " ".join(sys.argv[1:])
    
    console.print(Panel(f"[bold cyan]Input Task:[/bold cyan]\n{user_task}", expand=False))

    try:
        with Live(Spinner("dots", text="AgentForge is thinking..."), refresh_per_second=10, console=console) as live:
            response = run_agent(user_task)
            live.stop()

        # Display Summary
        status_color = "green" if response.valid else "red"
        status_icon = "âœ…" if response.valid else "âŒ"
        
        console.print(Panel(
            f"[bold {status_color}]{status_icon} Summary:[/bold {status_color}]\n{response.summary}",
            title="Final Response",
            border_style=status_color
        ))

        # Display Tool Results
        table = Table(title="Execution Details", box=None)
        table.add_column("Tool", style="magenta")
        table.add_column("Status", style="bold")
        table.add_column("Details", style="italic")

        for res in response.results:
            status = "[green]SUCCESS[/green]" if res.success else f"[red]FAILED[/red]"
            details = str(res.output)[:100] + ("..." if len(str(res.output)) > 100 else "")
            if res.error:
                details = f"[red]{res.error}[/red]"
            
            table.add_row(res.tool, status, details)

        console.print(table)

    except Exception as e:
        console.print(Panel(f"[bold red]System Error:[/bold red] {str(e)}", title="Failure"))
        sys.exit(1)

if __name__ == "__main__":
    main()
