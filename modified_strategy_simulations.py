#!/usr/bin/env python3
"""
100 Modified Investment Game Simulations with Distribution Analysis
Modified Strategy: Bet exactly 50% of current balance on each flip
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Set seed for reproducibility
np.random.seed(42)

# Parameters
initial_balance = 1000
age_start = 25
age_end = 55
years = age_end - age_start
n_simulations = 100

def simulate_modified_investment_game(initial, years):
    """
    Simulate the MODIFIED investment game for a given number of years.
    Strategy: Bet exactly 50% of current balance on each flip
    - If heads (50%): the 50% bet increases by 50% (becomes 75% of original balance)
    - If tails (50%): the 50% bet decreases by 40% (becomes 30% of original balance)
    - Final balance = 50% (unbet portion) + bet outcome
    """
    balance = initial
    path = [initial]
    ages = [age_start]
    coin_flips = []
    bet_amounts = []
    
    for year in range(years):
        # Calculate 50% bet amount
        bet_amount = balance * 0.5
        unbet_amount = balance * 0.5
        
        # Flip coin (1 = heads, 0 = tails)
        coin_flip = np.random.binomial(1, 0.5)
        coin_flips.append(coin_flip)
        bet_amounts.append(bet_amount)
        
        # Update balance based on coin flip
        if coin_flip == 1:  # Heads - bet increases by 50%
            bet_outcome = bet_amount * 1.5  # 50% * 1.5 = 75% of original balance
        else:  # Tails - bet decreases by 40%
            bet_outcome = bet_amount * 0.6  # 50% * 0.6 = 30% of original balance
            
        # New balance = unbet portion + bet outcome
        balance = unbet_amount + bet_outcome
            
        path.append(balance)
        ages.append(age_start + year + 1)
    
    return ages, path, coin_flips, bet_amounts

def run_modified_simulations(n_sims, initial, years):
    """
    Run multiple modified strategy simulations and return final balances
    """
    final_balances = []
    all_paths = []
    
    for sim in range(n_sims):
        ages, path, flips, bets = simulate_modified_investment_game(initial, years)
        final_balances.append(path[-1])
        all_paths.append({
            'simulation': sim + 1,
            'ages': ages,
            'balances': path,
            'final_balance': path[-1],
            'heads_count': sum(flips),
            'tails_count': len(flips) - sum(flips)
        })
    
    return final_balances, all_paths

# Run 100 modified strategy simulations
print("Running 100 modified strategy simulations...")
modified_final_balances, modified_paths = run_modified_simulations(n_simulations, initial_balance, years)

# Create data frame for analysis
modified_sim_data = pd.DataFrame({
    'simulation': range(1, n_simulations + 1),
    'final_balance': modified_final_balances
})

# Calculate statistics
mean_balance = np.mean(modified_final_balances)
median_balance = np.median(modified_final_balances)
std_balance = np.std(modified_final_balances)
prob_above_initial = np.mean(np.array(modified_final_balances) > initial_balance)
prob_above_10000 = np.mean(np.array(modified_final_balances) > 10000)

# Create object-oriented matplotlib plot
fig, ax = plt.subplots(figsize=(14, 10))

# Group values above 10000 together for better visualization
grouped_balances = [min(balance, 10000) for balance in modified_final_balances]

# Create histogram with smaller buckets and linear scale
n, bins, patches = ax.hist(grouped_balances, bins=50, alpha=0.7, color='darkgreen', 
                          edgecolor='black', linewidth=0.8, density=False)

# Color bars based on value ranges
for i, (patch, bin_left, bin_right) in enumerate(zip(patches, bins[:-1], bins[1:])):
    bin_center = (bin_left + bin_right) / 2
    if bin_center > 10000:
        patch.set_facecolor('purple')
        patch.set_alpha(0.6)
    elif bin_center > initial_balance:
        patch.set_facecolor('green')
        patch.set_alpha(0.6)
    elif bin_center > 100:
        patch.set_facecolor('orange')
        patch.set_alpha(0.6)
    else:
        patch.set_facecolor('red')
        patch.set_alpha(0.6)

# Add vertical lines for key thresholds
ax.axvline(initial_balance, color='red', linestyle='--', linewidth=3, 
           alpha=0.8, label=f'Initial Balance (${initial_balance:,})')
ax.axvline(10000, color='purple', linestyle=':', linewidth=3, 
           alpha=0.8, label='$10,000+ (Grouped)')
ax.axvline(mean_balance, color='blue', linestyle='-', linewidth=3, 
           alpha=0.8, label=f'Mean (${mean_balance:,.0f})')
ax.axvline(median_balance, color='orange', linestyle='-', linewidth=3, 
           alpha=0.8, label=f'Median (${median_balance:,.0f})')

# Customize the plot
ax.set_title('Distribution of Final Account Balances at Age 55\n100 Simulations of MODIFIED Investment Game (50% Betting Strategy - Values >$10,000 Grouped)', 
             fontsize=18, fontweight='bold', pad=25)

ax.set_xlabel('Final Account Balance ($)', fontsize=16, fontweight='bold')
ax.set_ylabel('Frequency', fontsize=16, fontweight='bold')

# Format x-axis as currency
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))

# Use linear scale and set appropriate limits
ax.set_xlim(0, 10500)

# Add grid
ax.grid(True, alpha=0.3, linestyle='-', linewidth=0.8)

# Add legend
ax.legend(fontsize=14, loc='upper right', framealpha=0.9)

# Add some styling
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_linewidth(2)
ax.spines['bottom'].set_linewidth(2)

# Add text box with key statistics
stats_text = f"""Modified Strategy Results (n=100):
• Mean: ${mean_balance:,.0f}
• Median: ${median_balance:,.0f}
• Std Dev: ${std_balance:,.0f}
• P(Balance > $1,000): {prob_above_initial:.1%}
• P(Balance > $10,000): {prob_above_10000:.1%}
• Min: ${min(modified_final_balances):,.0f}
• Max: ${max(modified_final_balances):,.0f}"""

ax.text(0.02, 0.98, stats_text, 
        transform=ax.transAxes, 
        fontsize=12,
        verticalalignment='top',
        bbox=dict(boxstyle="round,pad=0.5", facecolor='lightgreen', alpha=0.8))

plt.tight_layout()

# Save the plot
plt.savefig('modified_strategy_distribution.png', dpi=300, bbox_inches='tight')
plt.show()

# Print detailed results
print("="*80)
print("100 MODIFIED STRATEGY SIMULATIONS RESULTS")
print("="*80)
print(f"Strategy: Bet exactly 50% of balance on each flip")
print(f"Number of Simulations: {n_simulations}")
print(f"Initial Balance: ${initial_balance:,.2f}")
print(f"Mean Final Balance: ${mean_balance:,.2f}")
print(f"Median Final Balance: ${median_balance:,.2f}")
print(f"Standard Deviation: ${std_balance:,.2f}")
print(f"Minimum Final Balance: ${min(modified_final_balances):,.2f}")
print(f"Maximum Final Balance: ${max(modified_final_balances):,.2f}")

print(f"\nProbability Analysis:")
print(f"P(Balance > $1,000): {prob_above_initial:.1%}")
print(f"P(Balance > $10,000): {prob_above_10000:.1%}")
print(f"P(Balance > $100): {np.mean(np.array(modified_final_balances) > 100):.1%}")

# Count simulations by outcome categories
profitable_sims = np.sum(np.array(modified_final_balances) > initial_balance)
high_value_sims = np.sum(np.array(modified_final_balances) > 10000)
catastrophic_sims = np.sum(np.array(modified_final_balances) < 100)
moderate_sims = n_simulations - profitable_sims - catastrophic_sims

print(f"\nOutcome Categories:")
print(f"High Value (>$10,000): {high_value_sims} simulations ({high_value_sims/n_simulations:.1%})")
print(f"Profitable (>$1,000): {profitable_sims} simulations ({profitable_sims/n_simulations:.1%})")
print(f"Moderate ($100-$1,000): {moderate_sims} simulations ({moderate_sims/n_simulations:.1%})")
print(f"Catastrophic (<$100): {catastrophic_sims} simulations ({catastrophic_sims/n_simulations:.1%})")

print("\n" + "="*80)
print("COMPARISON WITH ORIGINAL STRATEGY")
print("="*80)

# Load original strategy results for comparison
# (These would be the results from multiple_simulations.py)
original_prob_above_1000 = 0.31  # From previous analysis
original_prob_above_10000 = 0.06  # From previous analysis

print(f"Original Strategy (100% betting):")
print(f"  P(Balance > $1,000): {original_prob_above_1000:.1%}")
print(f"  P(Balance > $10,000): {original_prob_above_10000:.1%}")

print(f"\nModified Strategy (50% betting):")
print(f"  P(Balance > $1,000): {prob_above_initial:.1%}")
print(f"  P(Balance > $10,000): {prob_above_10000:.1%}")

print(f"\nComparison:")
if prob_above_initial > original_prob_above_1000:
    print(f"✅ P(Balance > $1,000) is HIGHER in modified strategy")
else:
    print(f"❌ P(Balance > $1,000) is LOWER in modified strategy")

if prob_above_10000 > original_prob_above_10000:
    print(f"✅ P(Balance > $10,000) is HIGHER in modified strategy")
else:
    print(f"❌ P(Balance > $10,000) is LOWER in modified strategy")

print(f"\nAnalysis:")
print(f"• Modified strategy reduces risk by only betting 50% of balance")
print(f"• This creates a 'safety net' of 50% that's never at risk")
print(f"• However, it also limits upside potential")
print(f"• The trade-off between risk reduction and return potential is evident")

print("\n" + "="*80)
print("ANALYSIS & COMMENTARY")
print("="*80)

if prob_above_10000 > original_prob_above_10000:
    print("✅ MODIFIED STRATEGY PERFORMANCE: BETTER!")
    print(f"   Higher probability of reaching $10,000+ ({prob_above_10000:.1%} vs {original_prob_above_10000:.1%})")
    happiness = "😊 HAPPY - Modified strategy shows improvement!"
else:
    print("❌ MODIFIED STRATEGY PERFORMANCE: WORSE!")
    print(f"   Lower probability of reaching $10,000+ ({prob_above_10000:.1%} vs {original_prob_above_10000:.1%})")
    happiness = "😐 MIXED - Modified strategy has trade-offs!"

print(f"\n{happiness}")

print(f"\nKey Insights:")
print(f"• Risk management through partial betting affects both upside and downside")
print(f"• The 50% safety net prevents total ruin but limits explosive growth")
print(f"• Modified strategy shows different risk-return characteristics")
print(f"• This demonstrates the importance of position sizing in investment strategies")

# Show first 10 simulation results
print(f"\nFirst 10 Modified Strategy Simulation Results:")
print("-" * 60)
for i in range(min(10, n_simulations)):
    sim_result = modified_paths[i]
    print(f"Sim {i+1:2d}: ${sim_result['final_balance']:8,.2f} "
          f"(H:{sim_result['heads_count']:2d}, T:{sim_result['tails_count']:2d})")

print("\n" + "="*80)
