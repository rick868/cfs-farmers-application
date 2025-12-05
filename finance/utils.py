def calculate_repayment(amount, months, interest_rate=12):
    """
    Calculates monthly repayment with simple interest.
    Interest Rate default is 12% per annum.
    """
    rate_per_month = (interest_rate / 100) / 12
    # Simple interest formula for estimation
    total_interest = float(amount) * (interest_rate / 100) * (int(months) / 12)
    total_payable = float(amount) + total_interest
    monthly_installment = total_payable / int(months)
    
    return {
        "monthly_installment": round(monthly_installment, 2),
        "total_payable": round(total_payable, 2),
        "total_interest": round(total_interest, 2)
    }

def calculate_premium(crop, acreage, coverage_amount):
    """
    Calculates insurance premium based on crop risk factor.
    """
    # Risk factors (percentages of coverage amount)
    risk_factors = {
        'MAIZE': 0.05,  # 5%
        'BEANS': 0.06,
        'TEA': 0.03,
        'COFFEE': 0.04
    }
    
    rate = risk_factors.get(crop, 0.05)
    premium = float(coverage_amount) * rate
    
    return {
        "premium": round(premium, 2),
        "rate_percentage": rate * 100
    }
