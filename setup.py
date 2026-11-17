from setuptools import setup, find_packages

setup(
    name="frappe-data-center-pue-rack-dcim-billing",
    version="1.0.0",
    description="Frappe DCIM Engine: Colocation Rack Density, Power Usage Effectiveness (PUE) Monitoring & 3-Phase Branch Circuit Power Billing.",
    author="Shyam Kumar Pandey",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False
)
