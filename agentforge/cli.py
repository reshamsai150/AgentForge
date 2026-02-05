import sys
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.spinner import Spinner
from .main import run_agent

console = Console()

def run_with_task(user_task: str):
    try:
        console.print(Panel(f"[bold cyan]Input Task:[/bold cyan]\n{user_task}", expand=False))

        with Live(Spinner("dots", text="AgentForge is thinking..."), refresh_per_second=10, console=console) as live:
            response = run_agent(user_task)
            live.stop()

        # Display Summary
        status_color = "green" if response.valid else "red"
        status_icon = "✅" if response.valid else "❌"
        
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

        if response.results:
            for res in response.results:
                status = "[green]SUCCESS[/green]" if res.success else f"[red]FAILED[/red]"
                details = str(res.output)[:100] + ("..." if len(str(res.output)) > 100 else "")
                if res.error:
                    details = f"[red]{res.error}[/red]"
                
                table.add_row(res.tool, status, details)

        console.print(table)

    except Exception as e:
        # Fallback to plain print if Rich fails (handles the "too many values to unpack" issue)
        print(f"\n--- Result ---\n{user_task}")
        try:
            from agentforge.main import run_agent
            resp = run_agent(user_task)
            print(f"Summary: {resp.summary}")
            print(f"Valid: {resp.valid}")
        except Exception as inner_e:
            print(f"System Error: {str(e)} / {str(inner_e)}")

def main():
    user_task = " ".join(sys.argv[1:])
    run_with_task(user_task)

if __name__ == "__main__":
    main()
