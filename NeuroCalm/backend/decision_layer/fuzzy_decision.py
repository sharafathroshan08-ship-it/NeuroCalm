# ============================================================
# NEUROCALM - FUZZY DECISION LAYER
# ============================================================

def fuzzy_decision(score):

    # ----------------------------------------
    # Fuzzy membership values
    # ----------------------------------------

    low = max(0, min(1, (50 - score) / 50))

    moderate = max(
        0,
        min(
            1,
            1 - abs(score - 50) / 17
        )
    )

    high = max(0, min(1, (score - 50) / 50))

    memberships = {
        "Low": round(low, 2),
        "Moderate": round(moderate, 2),
        "High": round(high, 2)
    }

    # ----------------------------------------
    # Final decision
    # ----------------------------------------

    if score <= 33:
        final_level = "Low"

    elif score <= 66:
        final_level = "Moderate"

    else:
        final_level = "High"

    return final_level, memberships


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("NEUROCALM - FUZZY DECISION LAYER")
    print("=" * 60)

    score = float(
        input("\nEnter stress score (0-100): ")
    )

    level, memberships = fuzzy_decision(score)

    print("\nFuzzy Membership:")
    print("Low     :", memberships["Low"])
    print("Moderate:", memberships["Moderate"])
    print("High    :", memberships["High"])

    print("\nFinal Stress Level:", level)

    print("\n✅ Fuzzy Decision completed!")