import json

# Votre string JSON
data = '''{
  "DominantColor": {
    "Theme": "Dark"
  },
  "PrimaryShapesAndElementSizes": [
    {
      "Shape": "Rectangle",
      "Description": "Book Now button",
      "RelativeSizePercentage": 15
    },
    {
      "Shape": "Rectangle",
      "Description": "Read More button",
      "RelativeSizePercentage": 15
    },
    {
      "Shape": "Navigation Bar",
      "Description": "Bottom navigation menu with icons",
      "RelativeSizePercentage": 10
    }
  ],
  "Layout": {
    "GeneralStructure": "Vertical stack with header, main content, and bottom navigation",
    "ElementAlignment": "Center-aligned content with consistent margins",
    "WhitespaceUtilization": "Well-balanced negative space between sections enhancing readability"
  },
  "GeneralStyle": {
    "Category": "Activities"
  },
  "Navigation": {
    "Placement": "Bottom fixed navigation bar",
    "VisualElements": ["Home icon", "Calendar icon", "Treatment icon", "More options icon"],
    "Style": "Modern minimal icon-based navigation with labels"
  },
  "VisualHierarchy": [
    {
      "Element": "Name Header",
      "Priority": 1,
      "Reason": "Large typography at the top establishes brand identity"
    },
    {
      "Element": "Schedule Appointment CTA",
      "Priority": 2,
      "Reason": "Prominent positioning and contrasting button color"
    },
    {
      "Element": "About Me Section",
      "Priority": 3,
      "Reason": "Detailed text providing key information"
    },
    {
      "Element": "Navigation Bar",
      "Priority": 4,
      "Reason": "Essential but subtle navigation elements at bottom"
    }
  ]
}'''

# Charger la chaîne JSON dans un dictionnaire
parsed_data = json.loads(data)

# Construire les variables sous forme de chaînes concaténées
DominantColor_Theme = f"Theme: {parsed_data['DominantColor']['Theme']}"

PrimaryShapesAndElementSizes = " | ".join([
    f"Shape: {item['Shape']}, Description: {item['Description']}, RelativeSizePercentage: {item['RelativeSizePercentage']}%"
    for item in parsed_data['PrimaryShapesAndElementSizes']
])

Layout = f"GeneralStructure: {parsed_data['Layout']['GeneralStructure']} | " \
         f"ElementAlignment: {parsed_data['Layout']['ElementAlignment']} | " \
         f"WhitespaceUtilization: {parsed_data['Layout']['WhitespaceUtilization']}"

GeneralStyle_Category = f"Category: {parsed_data['GeneralStyle']['Category']}"

Navigation = f"Placement: {parsed_data['Navigation']['Placement']} | " \
            f"VisualElements: {', '.join(parsed_data['Navigation']['VisualElements'])} | " \
            f"Style: {parsed_data['Navigation']['Style']}"

VisualHierarchy = " | ".join([
    f"Element: {item['Element']}, Priority: {item['Priority']}, Reason: {item['Reason']}"
    for item in parsed_data['VisualHierarchy']
])

# Exemple d'affichage
print("DominantColor:", DominantColor_Theme)
print("PrimaryShapesAndElementSizes:", PrimaryShapesAndElementSizes)
print("Layout:", Layout)
print("GeneralStyle_Category:", GeneralStyle_Category)
print("Navigation:", Navigation)
print("VisualHierarchy:", VisualHierarchy)
