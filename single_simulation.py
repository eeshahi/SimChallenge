import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Set seed for reproducibility
np.random.seed(42)

# Parameters
initial_balance = 1000
age_start = 25  # Starting age
age_end = 55    # Ending age
years = age_end - age_start

# Simulate one path of the investment game
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

# Run simulation
ages, balances, flips = simulate_investment_game(initial_balance, years)

# Create data frame for analysis
sim_data = pd.DataFrame({
    'age': ages,
    'balance': balances,
    'year': range(len(ages))
})

# Create object-oriented matplotlib plot
fig, ax = plt.subplots(figsize=(12, 8))

# Plot the balance over time
ax.plot(sim_data['age'], sim_data['balance'], 
        color='darkblue', linewidth=2.5, marker='o', markersize=6,
        label='Account Balance')

# Add horizontal line for initial balance
ax.axhline(y=initial_balance, color='red', linestyle='--', linewidth=2, 
           alpha=0.7, label='Initial Balance ($1,000)')

# Add horizontal line for break-even
ax.axhline(y=initial_balance, color='green', linestyle=':', linewidth=2, 
           alpha=0.7, label='Break-even Point')

# Customize the plot
ax.set_title('Investment Game: Account Balance Over Time\nSingle Simulation Path', 
             fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Age', fontsize=14, fontweight='bold')
ax.set_ylabel('Account Balance ($)', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)
ax.legend(fontsize=12, loc='upper left')

# Format y-axis as currency
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))

# Set x-axis to show every 5 years
ax.set_xticks(range(age_start, age_end + 1, 5))

# Add some styling
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_linewidth(1.5)
ax.spines['bottom'].set_linewidth(1.5)

# Add text annotation for final balance
final_balance = balances[-1]
ax.annotate(f'Final Balance: ${final_balance:,.2f}', 
            xy=(age_end, final_balance), xytext=(age_end-5, final_balance + 200),
            arrowprops=dict(arrowstyle='->', color='darkblue', lw=2),
            fontsize=12, fontweight='bold', color='darkblue',
            bbox=dict(boxstyle="round,pad=0.3", facecolor='lightblue', alpha=0.7))

plt.tight_layout()
plt.show()

# Print detailed results
print("="*60)
print("SINGLE SIMULATION RESULTS")
print("="*60)
print(f"Initial Balance: ${initial_balance:,.2f}")
print(f"Final Balance: ${final_balance:,.2f}")
print(f"Total Return: ${final_balance - initial_balance:,.2f}")
print(f"Percentage Return: {((final_balance / initial_balance) - 1) * 100:.2f}%")
print(f"Number of Heads: {sum(flips)} out of {len(flips)} flips")
print(f"Number of Tails: {len(flips) - sum(flips)} out of {len(flips)} flips")
print(f"Head Percentage: {sum(flips)/len(flips)*100:.1f}%")

# Show the path
print("\nYear-by-Year Results:")
print("-" * 40)
for i, (age, balance) in enumerate(zip(ages, balances)):
    if i == 0:
        print(f"Age {age}: ${balance:,.2f} (Initial)")
    else:
        outcome = "Heads (+50%)" if flips[i-1] == 1 else "Tails (-40%)"
        print(f"Age {age}: ${balance:,.2f} ({outcome})")

print("\n" + "="*60)
print("ANALYSIS")
print("="*60)

if final_balance > initial_balance:
    print("✅ RESULT: PROFITABLE!")
    print(f"   You gained ${final_balance - initial_balance:,.2f} over {years} years")
    print("   This simulation was lucky - you got more heads than tails")
else:
    print("❌ RESULT: LOSS!")
    print(f"   You lost ${initial_balance - final_balance:,.2f} over {years} years")
    print("   This simulation was unlucky - you got more tails than heads")

print(f"\nExpected value per year: ${initial_balance * 0.05:,.2f}")
print(f"Actual average per year: ${(final_balance - initial_balance) / years:,.2f}")

# Show the data
print("\nDetailed Data:")
print(sim_data.round(2))
