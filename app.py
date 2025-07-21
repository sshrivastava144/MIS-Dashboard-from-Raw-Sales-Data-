from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

def plot_to_base64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    encoded = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    return encoded

@app.route('/')
def dashboard():
    df = pd.read_csv('sales_data.csv', sep='\t')
    df.columns = df.columns.str.strip()
    df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')
    df = df.dropna(subset=['Order Date', 'Region', 'Salesperson', 'Product', 'Order Value'])
    df['Month-Year'] = df['Order Date'].dt.to_period('M')

    # Aggregated data
    monthly_sales = df.groupby('Month-Year')['Order Value'].sum().sort_index()
    top_products = df.groupby('Product')['Order Value'].sum().nlargest(5)
    region_sales = df.groupby('Region')['Order Value'].sum()
    salesperson_sales = df.groupby('Salesperson')['Order Value'].sum()

    # Graphs
    fig1, ax1 = plt.subplots()
    monthly_sales.plot(ax=ax1, marker='o', title='Month-on-Month Sales')
    fig1.tight_layout()
    chart_monthly = plot_to_base64(fig1)

    fig2, ax2 = plt.subplots()
    top_products.plot(kind='bar', ax=ax2, title='Top 5 Products')
    fig2.tight_layout()
    chart_products = plot_to_base64(fig2)

    fig3, ax3 = plt.subplots()
    region_sales.plot(kind='bar', ax=ax3, title='Region-wise Sales')
    fig3.tight_layout()
    chart_regions = plot_to_base64(fig3)

    fig4, ax4 = plt.subplots()
    salesperson_sales.plot(kind='bar', ax=ax4, title='Salesperson-wise Sales')
    fig4.tight_layout()
    chart_salespersons = plot_to_base64(fig4)

    return render_template("dashboard.html",
                           monthly_sales=monthly_sales,
                           top_products=top_products,
                           region_sales=region_sales,
                           salesperson_sales=salesperson_sales,
                           chart_monthly=chart_monthly,
                           chart_products=chart_products,
                           chart_regions=chart_regions,
                           chart_salespersons=chart_salespersons)

if __name__ == '__main__':
    app.run(debug=True)
