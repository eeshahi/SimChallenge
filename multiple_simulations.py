#!/usr/bin/env python3
"""
100 Investment Game Simulations with Distribution Analysis
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

def simulate_investment_game(initial, years):
    """
    Simulate the investment game for a given number of years.
    Heads (50%): multiply by 1.5
    Tails (50%): multiply by 0.6
    """
    balance = initial
    path = [initial]
    ages = [age_start]
    coin_flips = []
    
    for year in range(years):
        # Flip coin (1 = heads, 0 = tails)
        coin_flip = np.random.binomial(1, 0.5)
        coin_flips.append(coin_flip)
        
        # Update balance based on coin flip
        if coin_flip == 1:  # Heads
            balance = balance * 1.5
        else:  # Tails
            balance = balance * 0.6
            
        path.append(balance)
        ages.append(age_start + year + 1)
    
    return ages, path, coin_flips

def run_multiple_simulations(n_sims, initial, years):
    """
    Run multiple simulations and return final balances
    """
    final_balances = []
    all_paths = []
    
    for sim in range(n_sims):
        ages, path, flips = simulate_investment_game(initial, years)
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

# Run 100 simulations
print("Running 100 simulations...")
final_balances, all_paths = run_multiple_simulations(n_simulations, initial_balance, years)

# Create data frame for analysis
sim_data = pd.DataFrame({
    'simulation': range(1, n_simulations + 1),
    'final_balance': final_balances
})

# Calculate statistics
mean_balance = np.mean(final_balances)
median_balance = np.median(final_balances)
std_balance = np.std(final_balances)
prob_above_initial = np.mean(np.array(final_balances) > initial_balance)
prob_above_10000 = np.mean(np.array(final_balances) > 10000)

# Create object-oriented matplotlib plot
fig, ax = plt.subplots(figsize=(14, 10))

# Group values above 10000 together for better visualization
grouped_balances = [min(balance, 10000) for balance in final_balances]

# Create histogram with smaller buckets and linear scale
n, bins, patches = ax.hist(grouped_balances, bins=50, alpha=0.7, color='steelblue', 
                          edgecolor='black', linewidth=0.8, density=False)

# Color bars based on value ranges
for i, (patch, bin_left, bin_right) in enumerate(zip(patches, bins[:-1], bins[1:])):
    bin_center = (bin_left + bin_right) / 2
    if bin_center > initial_balance:
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
ax.set_title('Distribution of Final Account Balances at Age 55\n100 Simulations of Investment Game (Values >$10,000 Grouped)', 
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
stats_text = f"""Simulation Results (n=100):
• Mean: ${mean_balance:,.0f}
• Median: ${median_balance:,.0f}
• Std Dev: ${std_balance:,.0f}
• P(Balance > $1,000): {prob_above_initial:.1%}
• P(Balance > $10,000): {prob_above_10000:.1%}
• Min: ${min(final_balances):,.0f}
• Max: ${max(final_balances):,.0f}"""

ax.text(0.02, 0.98, stats_text, 
        transform=ax.transAxes, 
        fontsize=12,
        verticalalignment='top',
        bbox=dict(boxstyle="round,pad=0.5", facecolor='wheat', alpha=0.8))

plt.tight_layout()

# Save the plot
plt.savefig('multiple_simulations_distribution.png', dpi=300, bbox_inches='tight')
plt.show()

# Print detailed results
print("="*80)
print("100 SIMULATIONS RESULTS - INVESTMENT GAME DISTRIBUTION ANALYSIS")
print("="*80)
print(f"Number of Simulations: {n_simulations}")
print(f"Initial Balance: ${initial_balance:,.2f}")
print(f"Mean Final Balance: ${mean_balance:,.2f}")
print(f"Median Final Balance: ${median_balance:,.2f}")
print(f"Standard Deviation: ${std_balance:,.2f}")
print(f"Minimum Final Balance: ${min(final_balances):,.2f}")
print(f"Maximum Final Balance: ${max(final_balances):,.2f}")

print(f"\nProbability Analysis:")
print(f"P(Balance > $1,000): {prob_above_initial:.1%}")
print(f"P(Balance > $10,000): {prob_above_10000:.1%}")
print(f"P(Balance > $100): {np.mean(np.array(final_balances) > 100):.1%}")

# Count simulations by outcome categories
profitable_sims = np.sum(np.array(final_balances) > initial_balance)
catastrophic_sims = np.sum(np.array(final_balances) < 100)
moderate_sims = n_simulations - profitable_sims - catastrophic_sims

print(f"\nOutcome Categories:")
print(f"Profitable (>$1,000): {profitable_sims} simulations ({profitable_sims/n_simulations:.1%})")
print(f"Moderate ($100-$1,000): {moderate_sims} simulations ({moderate_sims/n_simulations:.1%})")
print(f"Catastrophic (<$100): {catastrophic_sims} simulations ({catastrophic_sims/n_simulations:.1%})")

print("\n" + "="*80)
print("ANALYSIS & COMMENTARY")
print("="*80)

if prob_above_initial > 0.5:
    print("✅ OVERALL RESULT: MOSTLY PROFITABLE!")
    print(f"   {prob_above_initial:.1%} of simulations ended above initial balance")
    happiness = "😊 HAPPY - Most simulations were profitable!"
else:
    print("❌ OVERALL RESULT: MOSTLY UNPROFITABLE!")
    print(f"   Only {prob_above_initial:.1%} of simulations ended above initial balance")
    happiness = "😱 NOT HAPPY - Most simulations resulted in losses!"

print(f"\n{happiness}")

print(f"\nKey Insights:")
print(f"• Expected value per year: ${initial_balance * 0.05:,.2f}")
print(f"• Actual mean return per year: ${(mean_balance - initial_balance) / years:,.2f}")
print(f"• Volatility is extreme: std dev = ${std_balance:,.0f}")
print(f"• {catastrophic_sims/n_simulations:.1%} of paths lead to near-total loss")

print(f"\nThis demonstrates the 'ergodicity problem' in economics:")
print(f"- Mathematical expectation suggests positive returns")
print(f"- Reality shows most paths lead to losses due to multiplicative effects")
print(f"- High volatility destroys wealth over time")
print(f"- This is why simulation is crucial for understanding complex systems!")

# Show first 10 simulation results
print(f"\nFirst 10 Simulation Results:")
print("-" * 50)
for i in range(min(10, n_simulations)):
    sim_result = all_paths[i]
    print(f"Sim {i+1:2d}: ${sim_result['final_balance']:8,.2f} "
          f"(H:{sim_result['heads_count']:2d}, T:{sim_result['tails_count']:2d})")

print("\n" + "="*80)
