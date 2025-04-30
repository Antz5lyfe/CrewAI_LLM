def get_target_website():
  """Asks the user for a website URL to target."""
  while True:
    website = input("Please enter the website URL you want to target: ")
    if website:
      return website
    else:
      print("You need to enter a website URL.")