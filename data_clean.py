import pandas as pd
import numpy as np

# Load your messy CSV file
df = pd.read_csv('data.csv')

print("🔍 RAW DATA INSPECTION")
print(f"Shape: {df.shape}")
print("\nColumns:", df.columns.tolist())
print("\nFirst 3 rows:")
print(df.head(3))

# CLEANING STEP 1: Fix #REF! errors
df = df.replace('#REF!', 'No Response')

# CLEANING STEP 2: Focus on Category columns only
category_cols = [col for col in df.columns if 'Category' in str(col)]
print(f"\n📊 Found {len(category_cols)} category columns")

# CLEANING STEP 3: Melt to long format (all feedback in one column)
feedback_long = df.melt(id_vars=['IDQ44'], value_vars=category_cols, 
                       var_name='Question', value_name='Feedback')

# CLEANING STEP 4: Remove empty/no response
feedback_clean = feedback_long[feedback_long['Feedback'] != 'No Response'].copy()

print(f"\n✅ CLEANED DATA: {len(feedback_clean)} valid responses")

# ANALYSIS: Count top categories
top_categories = feedback_clean['Feedback'].value_counts().head(15)
total_responses = len(feedback_clean)

summary_stats = pd.DataFrame({
    'Rank': range(1, len(top_categories)+1),
    'Category': top_categories.index,
    'Count': top_categories.values,
    'Percentage': (top_categories.values / total_responses * 100).round(1)
})

# SAVE CLEAN SUMMARY
summary_stats.to_csv('summary_stats.csv', index=False)
print("\n🎉 SUMMARY STATS SAVED to summary_stats.csv")
print("\n📈 TOP 10 CATEGORIES:")
print(summary_stats.head(10).to_string(index=False))

# Export full cleaned data too
feedback_clean.to_csv('cleaned_feedback.csv', index=False)
print("\n💾 Full cleaned data saved to cleaned_feedback.csv")


