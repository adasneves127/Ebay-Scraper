import os
import urllib.request, urllib.parse                                                                             #Import our needed libraries
import re           
import webbrowser                                                                                               #We use urllib request, and parse, as well as re for regular expressions

def OSFind():
    from platform import system as sys
    systemType = sys().lower()
    
    if systemType == "darwin":
        return "MacOS"
    elif systemType == "linux":
        return systemType
    elif systemType == "windows":
        return systemType
    else:
        return "OS Could not be determined!"

url = ""    
Output = open("Output.csv", "w")
OutputHTML = open("Output.html", "w")                                                                                                 #Create a blank string named URL
AdvancedSearch = True if str.lower(input("Would you like Advanced Search Tools? (Y, N) ")) == "y" else False    #Ask if we are going to use advanced search.
query = input("What would you like to search for? ")                                                            #Ask for our main search item
AdvancedQuery = ""
OutputHTML.write("""
<!DOCTYPE html>
    <html lang="en">
        <head>    
        <meta charset="UTF-8">    
        <meta http-equiv="X-UA-Compatible" content="IE=edge">    
        <meta name="viewport" content="width=device-width, initial-scale=1.0">    
        <title>Ebay Results: </title>
    </head>       
""")
#Write our HTML boiler plate code to our HTML file.

OutputHTML.write(f"<h3>Your Search: {query}</h3>")   
PriceLow = 0
PriceHigh = 0
Conditions = [  "New",
                "Open Box",
                "Certified Refurbished",
                "Seller Refurbished",
                "Used",
                "For parts or not working"]
ConditionCodes = [  1000,
                    1500,
                    2000,
                    2500,
                    3000,
                    7000]
if AdvancedSearch:
    PriceLow = input("What is the lowest price you would like to filter? $")
    AdvancedQuery += ("&_udlo=" + PriceLow) if PriceLow != "" else ""
    PriceHigh = input("What is the highest price you would like to filter? $")
    AdvancedQuery += ("&_udhi=" + PriceHigh) if PriceHigh != "" else ""
    Material = True if input("Is there any material you would like to filter? (Y, N) ").lower() == "y" else False
    if Material:
        MatType = input("Which Material? ")
        AdvancedQuery += ("&Material=" + MatType) if MatType != "" else ""
    if input("Would you like to filter by condition? (Y, N) ").lower() == "y":
        print("Please enter the associated number for your search: ")
        for i in range(len(Conditions)):
            print(f"{i}: {Conditions[i]}")
        CondCode = int(input("? "))
        ConditionType = ConditionCodes[CondCode]   
    if input("Any results to exclude? (Y, N) ").lower() == "y":
        Exclusions = []
        CurrentExclude = ""
        print("Enter your excluding items. When done, type exit();")
        while True:
            CurrentExclude = input()
            if CurrentExclude.lower() == "exit();":
                break;
            else:
                Exclusions.append(CurrentExclude)

        for i in Exclusions:
            AdvancedQuery += f" -{i}"
            
    url = "https://www.ebay.com/sch/i.html?_nkw=" + query.replace(" ", "%20") + AdvancedQuery.replace(" ", "%20")
    
else:
    url = "https://www.ebay.com/sch/i.html?_nkw=" + query.replace(" ", "%20")


print(query)
print(url)
page = urllib.request.urlopen(url).read().decode("UTF-8")
Items = page.split("class=s-item__link href=")

Output.write("Item Name,Item Price,Item Link\n")
OutputHTML.write("""
    <body>    
        <table cellpadding="10", cellspacing="5">        
            <tr>            
                <th class="Name">Item Name</th>            
                <th class="Price">Item Price</th>            
                <th class="Link">Link</th>        
            </tr> """)

DisallowedChars = [',', ';', ':', '"', "'", "”"]

for i in range(len(Items)):
    if i != 0:
        Name = ""
        LinkRegex = re.match("http.*?><", Items[i])
        Link = LinkRegex.group(0)
        Link = Link[:Link.find("?")]
        #print(Link)
        if '<h3 class="s-item__title s-item__title--has-tags">' in Items[i]:
            Name = Items[i][Items[i].find('<h3 class="s-item__title s-item__title--has-tags">') + len ('<h3 class="s-item__title s-item__title--has-tags">') : Items[i].find("</h3>")]
        else:
            Name = Items[i][Items[i].find('<h3 class=s-item__title>') + len ('<h3 class=s-item__title>') : Items[i].find("</h3>")]
        PriceSplitHeadHelper = Items[i].split("<span class=s-item__price>")[1]
        Price = PriceSplitHeadHelper[0:PriceSplitHeadHelper.find("</span>")]
        

        if "<span class=LIGHT_HIGHLIGHT>" in Name:
            Name = Name[len("<span class=LIGHT_HIGHLIGHT>New Listing</span>")::]
        Name = Name.replace(",", ".")

        #Filter out our bad prices!...
        try:
            PriceRegex = re.match("\$[0-9,.]*", Price)
            i = 0
            while not "$" in PriceRegex.group(i):
                i += 1
            Price = PriceRegex.group(i)
        except AttributeError:
            True
        Price = Price.replace("<span class=ITALIC>", "")
        Name = Name.replace("&amp", "&")
        Name = Name.replace("<span class=BOLD>","")
        Name = Name.replace("</span>","")
        for char in DisallowedChars:
            if char in Name:
                Name = Name.replace(char, "")
            if char in Price:
                Price = Price.replace(char, "")
        
        

        print(f"Item: {Name}\n\tLink: {Link}\n\tPrice: {Price}\n")
        Output.write(f"{Name},{Price},{Link}\n")
        OutputHTML.write(f"<tr><td>{Name}</td><td>{Price}</td><td class='ItemButton'><button onclick='window.open(\"{Link}\")'>Link to Listing</button></td></tr>\n")

        #Filter out our bad spans...
        
        #print(Items[i])
OutputHTML.write("<style>button{background-color: #002ccb;color: white !important;border-radius: 10px; border: 1px solid black; box-shadow: 3px 3px black; font-family: Arial, Verdana, sans-serif; width: 100; } table{ width: 600px; } th, td{ padding: 7px 10px 10px 10px; } th{ text-transform: uppercase; letter-spacing: 0.1em; font-size: 90%; border-bottom: 2px solid #111111; border-top: 1px solid #999; text-align: left; } .ItemButton{ width: 8vw; } tr:nth-child(2n + 1){ background-color: #efefef; } tr:hover{ background-color: #ffeeee; }</style></body></html>")
Output.close();
OutputHTML.close();
OutputOption = input("Would you like to open results in [L]ibreOffice or [B]rowser?")
if OutputOption.lower() == "b":
    print(OSFind())
    if OSFind() == "Linux":
        os.system("firefox Output.html")
    elif OSFind() == "Windows":
        edge = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe %s'
        webbrowser.get(edge).open(f"file://{os.getcwd()}/Output.html")
    elif OSFind() == "MacOS":
        webbrowser.get('safari').open(f"file://{os.getcwd()}/Output.html")