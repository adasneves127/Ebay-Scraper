import os, urllib.request, urllib.parse, re, webbrowser                                                                 #Import all of our useful libraries                                                                                       

def OSFind():                                                                                                           #This function will be able to identify what OS is this running on
    from platform import system as sys                                                                                  #Only import one finction from platform, called system, and rename it to sys.
    systemType = sys().lower()                                                                                          #Get the system type that this is running on.
    if systemType == "darwin":                                                                                          #MacOS is called Darwin, but that's an easy fix...
        return "MacOS"                                                                                                      #Return the name as MacOS
    elif systemType == "linux":                                                                                         #All Linux Distros return the name as Linux, which makes this easy...
        return "Linux"                                                                                                      #Return the name as Linux
    elif systemType == "windows":                                                                                       #If we are running on Windows:
        return "Windows"                                                                                                    #Return the name as Windows
    else:                                                                                                               #If all these tests fail:
        return "OS Could not be determined!"                                                                                #This OS could not be determined...

url = ""                                                                                                                #This will be the variable in which we store our URL for searching
Output = open("Output.csv", "w", encoding="utf-8")                                                                      #Open a file called Output.csv for writing, and make sure we are using UTF-8 encoding
OutputHTML = open("Output.html", "w", encoding="utf-8")                                                                 #Open a file, HTML, write, UTF-8. Some listings have emoji, and python doesn't enjoy that sometimes.
AdvancedSearch = True if str.lower(input("Would you like Advanced Search Tools? (Y, N) ")) == "y" else False            #Ask if we are using Advanced Search Tools
query = input("What would you like to search for? ")                                                                    #Ask the user what they would like to search for
AdvancedQuery = ""                                                                                                      #Make a blank string called Advanced Query
OutputHTML.write("""
<!DOCTYPE html>
    <html lang="en">
        <head>    
        <meta charset="UTF-8">    
        <meta http-equiv="X-UA-Compatible" content="IE=edge">    
        <meta name="viewport" content="width=device-width, initial-scale=1.0">   
        <link rel="stylesheet" href="style.css" /> 
        <script src="Sorting.js"></script>
        <title>Ebay Results: </title>
       
""")                                                                                                                    #Write our HTML boiler plate code to our HTML file.

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
    OutputHTML.write("<ul>")
    if input("Any results to exclude? (Y, N) ").lower() == "y":  
        OutputHTML.write("<li>Excluded Results</li>")
        OutputHTML.write("<ul>")  
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
            OutputHTML.write(f"<li>{i}</li>")
        OutputHTML.write("</ul>")    
    PriceLow = input("What is the lowest price you would like to filter? $")
    AdvancedQuery += ("&_udlo=" + PriceLow) if PriceLow != "" else ""
    OutputHTML.write((f"<li>{PriceLow}</li>") if PriceLow != "" else "")
    PriceHigh = input("What is the highest price you would like to filter? $")
    AdvancedQuery += ("&_udhi=" + PriceHigh) if PriceHigh != "" else ""
    OutputHTML.write((f"<li>{PriceHigh}</li>") if PriceHigh != "" else "")
    Material = True if input("Is there any material you would like to filter? (Y, N) ").lower() == "y" else False
    if Material:
        MatType = input("Which Material? ")
        AdvancedQuery += ("&Material=" + MatType) if MatType != "" else ""
        OutputHTML.write((f"<li>Material: {Material}</li>") if MatType != "" else "")
    if input("Would you like to filter by condition? (Y, N) ").lower() == "y":
        print("Please enter the associated number for your search: ")
        for i in range(len(Conditions)):
            print(f"{i}: {Conditions[i]}")
        CondCode = int(input("? "))
        ConditionType = ConditionCodes[CondCode]   
        OutputHTML.write(f"<li>Condition: {Conditions[CondCode]}</li>")
    OutputHTML.write("</ul>")
            
    url = "https://www.ebay.com/sch/i.html?_nkw=" + query.replace(" ", "%20") + AdvancedQuery.replace(" ", "%20")
    
else:
    url = "https://www.ebay.com/sch/i.html?_nkw=" + query.replace(" ", "%20")

OutputHTML.write("<hr />")
print(query)
print(url)
page = urllib.request.urlopen(url).read().decode("UTF-8")
Items = page.split("class=s-item__link href=")

Output.write("Item Name,Item Price,Item Link\n")
OutputHTML.write("""
    </head>    
    <body>    
        <table id="myTable" cellpadding="10", cellspacing="5">        
            <tr>            
                <th class="Name" onClick="sortTable(0)">Item Name</th>            
                <th class="Price" onClick="sortTable(1)">Item Price</th>            
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
        OutputHTML.write(f"""
    <tr>
        <td>{Name}</td>
        <td>{Price}</td>
        <td class='ItemButton'>
            <button onclick='window.open(\"{Link}\")'>Link to Listing</button>
        </td>
    </tr>\n""")

        #Filter out our bad spans...
        
        #print(Items[i])
OutputHTML.write("</body></html>")
Output.close();
OutputHTML.close();
OutputOption = input("Press [Enter] to open in a browser!")

print(f"Current Operating System: {OSFind()}")
if OSFind() == "Linux":
    os.system("firefox Output.html")
elif OSFind() == "Windows":
    edge = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe %s'
    webbrowser.get(edge).open(f"file://{os.getcwd()}/Output.html")
elif OSFind() == "MacOS":
    webbrowser.get('safari').open(f"file://{os.getcwd()}/Output.html")