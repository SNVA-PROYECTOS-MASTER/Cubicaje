# -*- coding: utf-8 -*-
{
  "name": "SNVA - Packing Simulation",
  "summary": """
      Configure pallets and simulate optimal packing based on volume and weight constraints.
  """,
  "description": """
      The SNVA - Packing Simulation module allows you to define pallet configurations and simulate optimal packing for logistics and warehouse planning. 
      You can register various pallet dimensions, weight limits, and simulate how packages fit within those constraints.

      Key Features:
      - Define and manage custom pallet configurations (dimensions, weight capacity, etc.).
      - Simulate packing scenarios using selected pallets.
      - Visualize how packages are arranged based on the configured constraints.
      - Streamline logistics planning by ensuring optimal use of available space.
      - Supports integration with other logistics or inventory modules.

      Ideal for companies needing to optimize space usage in pallets during shipping or storage.
  """,
  "author": "SINOVA S.A.S",
  "email": 'soluciones.odoo@sinova.co',
  "website": 'https://www.sinova.co',
  'category': 'Website',
  'version': '1.0',
  'license': 'OPL-1', 
  'depends': ['web', 'base', 'stock'], 
  "data": [
        "security/ir.model.access.csv",
        "views/pallet_setting_data_views.xml",
        "views/res_config_settings_views.xml",
        "views/snva_pallet_simulation_views.xml",
        "views/snva_menu_options.xml",
        "views/snva_product_pallet_config_views.xml"
    ],
  'installable': True,
  'application': True,
}