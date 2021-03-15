query = "SELECT blood_bank, donor.blood_group, COUNT(*) " \
        "FROM blood, donor " \
        "WHERE givento_ID IS NULL AND " \
        "donatedby_ID = donor.ID " \
        "GROUP BY blood_bank, donor.blood_group"

print(query)
