import gradio as gr
import pandas as pd
import matplotlib.pyplot as plt
from carbon_model import calculate_carbon_value

listings = []
bids = []


def add_listing(name, land_acres, irrigation, crop_type, organic, soil_health):

    if not name:
        return "Please enter farmer name"

    total_carbon, price = calculate_carbon_value(
        land_acres, irrigation, organic, soil_health
    )

    listing = {
        "Farmer": name,
        "Land (Acres)": land_acres,
        "Crop": crop_type,
        "Irrigation": irrigation,
        "Organic": organic,
        "Soil Health": soil_health,
        "Carbon Credits (tons)": total_carbon,
        "AI Price (INR)": price,
        "Status": "Open"
    }

    listings.append(listing)

    return f"Listed | Carbon Credits: {total_carbon} tons | Value: ₹{price}"


def place_bid(company, farmer, bid_amount):

    for listing in listings:
        if listing["Farmer"] == farmer and listing["Status"] == "Open":

            ai_price = listing["AI Price (INR)"]

            if bid_amount >= ai_price:
                status = "Successful"
                listing["Status"] = "Sold"
            else:
                status = "Below Expected Price"

            bids.append({
                "Company": company,
                "Farmer": farmer,
                "Bid (INR)": bid_amount,
                "AI Price (INR)": ai_price,
                "Result": status
            })

            return f"Bid Result: {status}"

    return "Farmer Not Available"


def refresh_dropdown():
    open_farmers = [l["Farmer"] for l in listings if l["Status"] == "Open"]
    return gr.update(choices=open_farmers)


def show_dashboard():
    return pd.DataFrame(listings), pd.DataFrame(bids)


def generate_graph():

    if not listings:
        return None

    df = pd.DataFrame(listings)

    plt.figure()
    plt.bar(df["Farmer"], df["AI Price (INR)"])
    plt.xticks(rotation=45)
    plt.tight_layout()

    return plt


with gr.Blocks() as app:

    gr.Markdown("# AI Carbon Credit Marketplace")

    with gr.Tab("Farmer Portal"):

        name = gr.Textbox(label="Farmer Name")
        land = gr.Number(label="Land Size (Acres)")
        irrigation = gr.Dropdown(["Yes", "No"], label="Irrigation")
        crop = gr.Dropdown(["Rice", "Wheat", "Cotton", "Sugarcane"])
        organic = gr.Dropdown(["Yes", "No"], label="Organic")
        soil = gr.Slider(50, 100, label="Soil Health Score")

        submit = gr.Button("List Farm")
        output = gr.Textbox()

        submit.click(
            add_listing,
            inputs=[name, land, irrigation, crop, organic, soil],
            outputs=output
        )

    with gr.Tab("Corporate Bidding"):

        company = gr.Textbox(label="Company Name")
        farmer_dropdown = gr.Dropdown(label="Select Farmer")
        bid_amount = gr.Number(label="Bid Amount")

        refresh_btn = gr.Button("Refresh Farmers")
        bid_btn = gr.Button("Place Bid")
        bid_output = gr.Textbox()

        refresh_btn.click(refresh_dropdown, outputs=farmer_dropdown)
        bid_btn.click(
            place_bid,
            inputs=[company, farmer_dropdown, bid_amount],
            outputs=bid_output
        )

    with gr.Tab("Dashboard"):

        show_btn = gr.Button("Show Data")
        graph_btn = gr.Button("Show Graph")

        listing_table = gr.Dataframe()
        bid_table = gr.Dataframe()
        graph_output = gr.Plot()

        show_btn.click(show_dashboard, outputs=[listing_table, bid_table])
        graph_btn.click(generate_graph, outputs=graph_output)


if __name__ == "__main__":
    app.launch(debug=True)
