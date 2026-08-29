from django.shortcuts import render


def portal_home(request):
    projects = [
        {
            "title": "Qassim Digital Auction",
            "subtitle": "Digital auction platform for Qassim dates",
            "description": "A web-based auction system that supports live bidding, sellers, shops, buyers, and admin supervision.",
            "image": "auctions/img/project_qassim_auction.png",
            "url_name": "home",
        },
        {
            "title": "Malaria AI Detection",
            "subtitle": "AI-powered medical image classification",
            "description": "An artificial intelligence project that detects malaria from cell images using a trained deep learning model.",
            "image": "auctions/img/project_malaria_ai.png",
            "url_name": "malaria_home",
        },
        {
            "title": "Qassim Digital Auction Dashboard",
            "subtitle": "Interactive dashboard for auction insights",
            "description": "A dashboard project for visualizing auction-related data, branches, trading activity, and daily market indicators.",
            "image": "auctions/img/project_qassim_dashboard.png",
            "url_name": "qassim_dashboard_home",
        },
        {
            "title": "Sales Data Analysis and Engineering System",
            "subtitle": "Data analysis and database engineering",
            "description": "A data engineering and analytics system that processes sales data and presents interactive visual reports.",
            "image": "auctions/img/project_sales_analysis.png",
            "url_name": "sales_analysis_home",
        },
    ]


    return render(request, "portal/home.html", {"projects": projects})






def malaria_home(request):
    return render(request, "portal/coming_soon.html", {"project_name": "Malaria AI Detection"})


def qassim_dashboard_home(request):
    return render(request, "portal/coming_soon.html", {"project_name": "Qassim Digital Auction Dashboard"})


def sales_analysis_home(request):
    return render(request, "portal/coming_soon.html", {"project_name": "Sales Data Analysis and Engineering System"})