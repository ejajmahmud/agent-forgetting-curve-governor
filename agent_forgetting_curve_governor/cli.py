"""CLI for agent-forgetting-curve-governor."""
import sys
import argparse
from .governor import ForgettingGovernor


def main():
    parser = argparse.ArgumentParser(description="Agent Forgetting Curve Governor")
    parser.add_argument("--demo", action="store_true", help="Run forgetting curve demonstration")
    args = parser.parse_args()

    gov = ForgettingGovernor(prune_threshold=0.3)
    if args.demo:
        gov.record_memory("core_mission", "maintain_99.99_uptime", stability=10.0)
        gov.record_memory("temporary_chat", "user said hello", stability=0.1)
        # Simulate time passage
        sim_time = gov._items["temporary_chat"].last_accessed + 200.0
        pruned = gov.prune(current_time=sim_time)
        print("Pruned Stale Memories:", pruned)
        print("Remaining Memories:", gov.get_active_memories())
    else:
        parser.print_help()
    sys.exit(0)


if __name__ == "__main__":
    main()
