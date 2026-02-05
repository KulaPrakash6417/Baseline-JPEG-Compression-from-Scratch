def log_stage(title, before=None, after=None, next_step=None):
    print("\n" + "="*70)
    print(f"STAGE: {title}")
    print("="*70)

    if before is not None:
        print("\nBefore:")
        print(before)

    if after is not None:
        print("\nAfter:")
        print(after)

    if next_step is not None:
        print("\nNext:")
        print(next_step)

    print("="*70 + "\n")
