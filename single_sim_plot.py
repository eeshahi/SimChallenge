#!/usr/bin/env python3
"""
Single Investment Game Simulation with Object-Oriented Matplotlib Plot
"""

import random
import matplotlib.pyplot as plt
import numpy as np

# Set seed for reproducibility
random.seed(42)

# Parameters
initial_balance = 1000
age_start = 25  # Starting age
age_end = 55    # Ending age
years = age_end - age_start

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
        coin_flip = random.randint(0, 1)
        coin_flips.append(coin_flip)
        
        # Update balance based on coin flip
        if coin_flip == 1:  # Heads
            balance = balance * 1.5
        else:  # Tails
            balance = balance * 0.6
            
        path.append(balance)
        ages.append(age_start + year + 1)
    
    return ages, path, coin_flips

# Run simulation
ages, balances, flips = simulate_investment_game(initial_balance, years)

# Create object-oriented matplotlib plot
fig, ax = plt.subplots(figsize=(14, 10))

# Plot the balance over time with markers
line = ax.plot(ages, balances, 
               color='darkblue', 
               linewidth=3, 
               marker='o', 
               markersize=8,
               markerfacecolor='lightblue',
               markeredgecolor='darkblue',
               markeredgewidth=2,
               label='Account Balance',
               alpha=0.8)

# Add horizontal line for initial balance
ax.axhline(y=initial_balance, 
           color='red', 
           linestyle='--', 
           linewidth=3, 
           alpha=0.8, 
           label='Initial Balance ($1,000)')

# Add horizontal line for break-even
ax.axhline(y=initial_balance, 
           color='green', 
           linestyle=':', 
           linewidth=2, 
           alpha=0.6, 
           label='Break-even Point')

# Color-code points based on coin flip outcome
for i, (age, balance, flip) in enumerate(zip(ages[1:], balances[1:], flips)):
    color = 'green' if flip == 1 else 'red'
    ax.scatter(age, balance, 
               color=color, 
               s=100, 
               alpha=0.7, 
               edgecolors='black', 
               linewidth=1,
               zorder=5)

# Customize the plot
ax.set_title('Investment Game: Account Balance Over Time\nSingle Simulation Path (Ages 25-55)', 
             fontsize=18, fontweight='bold', pad=25)

ax.set_xlabel('Age', fontsize=16, fontweight='bold')
ax.set_ylabel('Account Balance ($)', fontsize=16, fontweight='bold')

# Format y-axis as currency
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))

# Set x-axis to show every 5 years
ax.set_xticks(range(age_start, age_end + 1, 5))
ax.set_xlim(age_start - 1, age_end + 1)

# Add grid
ax.grid(True, alpha=0.3, linestyle='-', linewidth=0.8)

# Add legend
ax.legend(fontsize=14, loc='upper left', framealpha=0.9)

# Add some styling
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_linewidth(2)
ax.spines['bottom'].set_linewidth(2)

# Add text annotation for final balance
final_balance = balances[-1]
ax.annotate(f'Final Balance: ${final_balance:,.2f}', 
            xy=(age_end, final_balance), 
            xytext=(age_end-8, final_balance + max(balances)*0.1),
            arrowprops=dict(arrowstyle='->', color='darkblue', lw=3),
            fontsize=14, fontweight='bold', color='darkblue',
            bbox=dict(boxstyle="round,pad=0.5", facecolor='lightblue', alpha=0.8))

# Add text box with key statistics
stats_text = f"""Simulation Results:
• Initial: ${initial_balance:,.0f}
• Final: ${final_balance:,.0f}
• Return: {((final_balance/initial_balance)-1)*100:.1f}%
• Heads: {sum(flips)}/{len(flips)} ({sum(flips)/len(flips)*100:.0f}%)
• Tails: {len(flips)-sum(flips)}/{len(flips)} ({(len(flips)-sum(flips))/len(flips)*100:.0f}%)"""

ax.text(0.02, 0.98, stats_text, 
        transform=ax.transAxes, 
        fontsize=12,
        verticalalignment='top',
        bbox=dict(boxstyle="round,pad=0.5", facecolor='wheat', alpha=0.8))

# Set y-axis to log scale to better show the dramatic decline
ax.set_yscale('log')
ax.set_ylim(0.1, max(balances) * 2)

plt.tight_layout()

# Save the plot
plt.savefig('single_simulation_plot.png', dpi=300, bbox_inches='tight')
plt.show()

# Print detailed results
print("="*70)
print("SINGLE SIMULATION RESULTS - INVESTMENT GAME")
print("="*70)
print(f"Initial Balance: ${initial_balance:,.2f}")
print(f"Final Balance: ${final_balance:,.2f}")
print(f"Total Return: ${final_balance - initial_balance:,.2f}")
print(f"Percentage Return: {((final_balance / initial_balance) - 1) * 100:.2f}%")
print(f"Number of Heads: {sum(flips)} out of {len(flips)} flips")
print(f"Number of Tails: {len(flips) - sum(flips)} out of {len(flips)} flips")
print(f"Head Percentage: {sum(flips)/len(flips)*100:.1f}%")

print("\nYear-by-Year Results:")
print("-" * 50)
for i, (age, balance) in enumerate(zip(ages, balances)):
    if i == 0:
        print(f"Age {age}: ${balance:,.2f} (Initial)")
    else:
        outcome = "Heads (+50%)" if flips[i-1] == 1 else "Tails (-40%)"
        print(f"Age {age}: ${balance:,.2f} ({outcome})")

print("\n" + "="*70)
print("ANALYSIS & COMMENTARY")
print("="*70)

if final_balance > initial_balance:
    print("✅ RESULT: PROFITABLE!")
    print(f"   You gained ${final_balance - initial_balance:,.2f} over {years} years")
    print("   This simulation was lucky - you got more heads than tails")
    happiness = "😊 HAPPY - This was a winning simulation!"
else:
    print("❌ RESULT: CATASTROPHIC LOSS!")
    print(f"   You lost ${initial_balance - final_balance:,.2f} over {years} years")
    print("   This simulation was unlucky - you got more tails than heads")
    happiness = "😱 NOT HAPPY AT ALL - This was a devastating loss!"

print(f"\nExpected value per year: ${initial_balance * 0.05:,.2f}")
print(f"Actual average per year: ${(final_balance - initial_balance) / years:,.2f}")

print(f"\n{happiness}")
print("\nThis simulation demonstrates the 'ergodicity problem' in economics:")
print("- Mathematical expectation suggests positive returns")
print("- Reality shows catastrophic losses due to multiplicative effects")
print("- Volatility drag destroys wealth over time")
print("- This is why simulation is crucial for understanding complex systems!")

