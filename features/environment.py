from utils.driver_manager import get_driver

def before_scenario(context, scenario):
    context.driver = get_driver()

def after_scenario(context, scenario):
    if hasattr(context, 'driver'):
        context.driver.quit()
