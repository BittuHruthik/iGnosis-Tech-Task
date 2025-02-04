import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


transactions = pd.read_csv('transaction_data.csv')
customers = pd.read_csv('purchase_behaviour.csv')


def get_top_products(df, n=3):
    product_sales = df.groupby('PROD_NAME').agg({
        'TOT_SALES': 'sum',
        'PROD_QTY': 'sum'
    }).sort_values('TOT_SALES', ascending=False)
    return product_sales.head(n)


def analyze_customer_segments(transactions_df, customers_df):
    
    customer_spending = transactions_df.groupby('LYLTY_CARD_NBR').agg({
        'TOT_SALES': 'sum',
        'TXN_ID': 'count'
    }).reset_index()
    customer_spending.columns = ['LYLTY_CARD_NBR', 'total_spent', 'transaction_count']
    
    
    customer_analysis = pd.merge(customer_spending, customers_df, on='LYLTY_CARD_NBR')
    
   
    segment_analysis = customer_analysis.groupby(['LIFESTAGE', 'PREMIUM_CUSTOMER']).agg({
        'total_spent': ['mean', 'count'],
        'transaction_count': 'mean'
    }).sort_values(('total_spent', 'mean'), ascending=False)
    
    return segment_analysis


def plot_insights(top_products, segment_analysis):
    
    plt.figure(figsize=(12, 6))
    top_products['TOT_SALES'].plot(kind='bar')
    plt.title('Top 3 Products by Sales')
    plt.xlabel('Product Name')
    plt.ylabel('Total Sales ($)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    
   
    segment_data = segment_analysis['total_spent']['mean'].unstack()
    plt.figure(figsize=(12, 6))
    sns.heatmap(segment_data, annot=True, fmt='.0f', cmap='YlOrRd')
    plt.title('Average Spending by Customer Segment')
    plt.tight_layout()
    plt.show()


def main():
    
    top_products = get_top_products(transactions)
    print("\nTop 3 Products by Sales:")
    print(top_products)
    

    segment_analysis = analyze_customer_segments(transactions, customers)
    print("\nCustomer Segment Analysis:")
    print(segment_analysis)
    
    
    plot_insights(top_products, segment_analysis)

if __name__ == "__main__":
    main()