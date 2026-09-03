def calculate_loan_payment(interest, term, pv):
    # interest: monthly interest rate as a decimal
    # term: number of payments
    # pv: present value (loan amount)
    
    if interest == 0:
        return pv / term
    
    payment = (pv * interest) / (1 - (1 + interest) ** -term)
    return payment