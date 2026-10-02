from PMJ.Stage2_CONSULT.PRECON_SUB_CATEGORY import sub_category

def test_validate_subcategory():
    assert sub_category.validate_subcategory("ITSR", "ITSR-ARCH") is True
    assert sub_category.validate_subcategory("ITSR", "CGRC-RASS") is False