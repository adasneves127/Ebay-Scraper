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

OutputHTML.write(f"<h3>Your Search: {query}</h3>")                                                                      #Write what our basic search was

Conditions = [  "New",                                                                                                  #Ebay has a list of conditions to filter by. These are their names
                "Open Box",
                "Certified Refurbished",
                "Seller Refurbished",
                "Used",
                "For parts or not working"]
ConditionCodes = [  1000,                                                                                               #For every condition there is, Ebay uses a code that corresponds to that condition.
                    1500,
                    2000,
                    2500,
                    3000,
                    7000]
if AdvancedSearch:
    AdvancedQuery, PriceLow, PriceHigh = "", 0, 0                                                                       #Make a blank string called Advanced Query
    OutputHTML.write("<ul>")                                                                                            #HTML Unordered List
    if input("Any results to exclude? (Y, N) ").lower() == "y":                                                         #If we want to exclude results
        OutputHTML.write("<li>Excluded Results</li>")                                                                   #Make a line item with the text "Excluded Results"
        OutputHTML.write("<ul>")                                                                                        #Make a sublist (Unordered) inside
        Exclusions = []                                                                                                 #Empty list, will hold our exclusions
        CurrentExclude = ""                                                                                             #Create a variable called Current Exclude
        print("Enter your excluding items. When done, submit a blank line")                                             #Inform the user that when we wish to be done with exclusions, to hit enter on a blank line.
        while True:                                                                                                     #Forever:
            CurrentExclude = input()                                                                                    #Set current Exclude to our input
            if CurrentExclude.lower() == "":                                                                            #If our input is the termination trigger
                break;                                                                                                  #Exit
            else:                                                                                                       #Otherwise
                Exclusions.append(CurrentExclude)                                                                       #Add this to our list, and restart the loop.
                
        for i in Exclusions:                                                                                            #For every item in exclusions:
            AdvancedQuery += f" -{i}"                                                                                   #Add it to our advanced query
            OutputHTML.write(f"<li>{i}</li>")                                                                           #Write a line item of our exclusion
        OutputHTML.write("</ul>")                                                                                       #When done, end the sublist
    PriceLow = input("What is the lowest price you would like to filter? $")                                            #Ask the user to enter the lowest price they wish to pay
    AdvancedQuery += ("&_udlo=" + PriceLow) if PriceLow != "" else ""                                                   #If they didn't submit a price, then dont do anything
    OutputHTML.write((f"<li>{PriceLow}</li>") if PriceLow != "" else "")                                                #If they didn't submit a price, then dont do anything
    PriceHigh = input("What is the highest price you would like to filter? $")                                          #Ask the user to enter the lowest price they wish to pay
    AdvancedQuery += ("&_udhi=" + PriceHigh) if PriceHigh != "" else ""                                                 #If they didn't submit a price, then dont do anything
    OutputHTML.write((f"<li>{PriceHigh}</li>") if PriceHigh != "" else "")                                              #If they didn't submit a price, then dont do anything
    Material = True if input("Is there any material you would like to filter? (Y, N) ").lower() == "y" else False       #If we want to filter by material
    if Material:                                                                                                        #
        MatType = input("Which Material? ")                                                                             #Ask which material
        AdvancedQuery += "&Material=" + MatType                                                                         #Add it to our query
        OutputHTML.write(f"<li>Material: {Material}</li>")                                                              #And to our HTML file
    if input("Would you like to filter by condition? (Y, N) ").lower() == "y":                                          #Filter by condition?
        print("Please enter the associated number for your search: ")                                                   #Tell the user to enter the number in which they want to filter by
        for i in range(len(Conditions)):                                                                                #For i in range of the length of the conditions,
            print(f"{i}: {Conditions[i]}")                                                                              #Print the index, follwed by the element at that index.
        CondCode = int(input("? "))                                                                                     #Wait for user input
        ConditionType = ConditionCodes[CondCode]                                                                        #Create the condition type
        OutputHTML.write(f"<li>Condition: {Conditions[CondCode]}</li>")                                                 #Write to our file
        AdvancedQuery += f"&LH_ItemCondition={CondCode}"                                                                #Add to the query                                     
    OutputHTML.write("</ul>")                                                                                           #End the list
            
    url = "https://www.ebay.com/sch/i.html?_nkw=" + query.replace(" ", "%20") + AdvancedQuery.replace(" ", "%20")       #Construct our url
else:                                                                                                                   #If we don't want to use our Advanced Search Tools
    url = "https://www.ebay.com/sch/i.html?_nkw=" + query.replace(" ", "%20")                                           #Construct our url

OutputHTML.write("<hr />")                                                                                              #Insert a Horizontal Rule (Line across the screen, used as a divider)
print(query)                                                                                                            #Print out our Query to the console
print(url)                                                                                                              #Print our URL to the screen
page = urllib.request.urlopen(url).read().decode("UTF-8")                                                               #Read the data from our target website
Items = page.split("class=s-item__link href=")                                                                          #Split the result by the CSS class and Link of s-item__link href=

Output.write("Item Name,Item Price,Item Link\n")                                                                        #Write to our CSV File our heading for each row
OutputHTML.write("""
    </head>    
    <body>    
        <table id="myTable" cellpadding="10", cellspacing="5">        
            <tr>            
                <th class="Name" onClick="sortTable(0)">Item Name</th>            
                <th class="Price" onClick="sortTable(1)">Item Price</th>            
                <th class="Link">Link</th>        
            </tr> """)                                                                                                  #More HTML base code, and HTML Table setup

DisallowedChars = [',', ';', ':', '"', "'", "”"]                                                                        #These are characters that can not be encoded in a CSV file, as they break the format.

for i in range(len(Items)):                                                                                             #For i in range of items
    if i != 0:                                                                                                          #If we are not on the first index, as that is garbaggio:
        Name = ""                                                                                                       #Create a blank string for our name
        LinkRegex = re.match("http.*?><", Items[i])                                                                     #This regex will match "http", followed by any character, until it finds ""><""
        Link = LinkRegex.group(0)                                                                                       #Get the first match of our regex
        Link = Link[:Link.find("?")]                                                                                    #There is sooooo much shit that isn't needed at the end of some of these URLs, so we just trim it out.
        if '<h3 class="s-item__title s-item__title--has-tags">' in Items[i]:                                            #If our item has weird tags, then we can filter that out...
            Name = Items[i][Items[i].find('<h3 class="s-item__title s-item__title--has-tags">') +                       #To filter, we can find where the start of the "has tags" element, 
                                 len ('<h3 class="s-item__title s-item__title--has-tags">') : Items[i].find("</h3>")]   #And add the length, and go all the way up until the end of the Heading 3 tag.
        else:                                                                                                           #Otherwise:
            Name = Items[i][Items[i].find('<h3 class=s-item__title>') +                                                 #Do the same thing, but just use the regular s-item__title tag
                                 len ('<h3 class=s-item__title>') : Items[i].find("</h3>")]                             #Adding the length, and going until the end of heading 3...
        PriceSplitHeadHelper = Items[i].split("<span class=s-item__price>")[1]                                          #Split this item on the "s-item__price" class, and get the first element in this list
        Price = PriceSplitHeadHelper[0:PriceSplitHeadHelper.find("</span>")]                                #Splice our string from 0 through till the end of the span...
        
        if "<span class=LIGHT_HIGHLIGHT>" in Name:                                                                      #If our item is a new listing
            Name = Name[len("<span class=LIGHT_HIGHLIGHT>New Listing</span>")::]                                        #Remove this from the string...
        Name = Name.replace(",", ".")                                                                                   #Replace all commas with periods.

        
        try:                                                                                                            #This needs to be in a Try:Except block, becuase if the regex finds no matches, then it gives an Attribute Error :(
            PriceRegex = re.match("\$[0-9,.]*", Price)                                                                  #The will match $ and any number 0-9, a comma, or a period, as many times as it can.
            i = 0                                                                                                       #This is going to be used for our group index in the while loop.
            while not "$" in PriceRegex.group(i):                                                                       #While we do not have a $ in the group we are looking through,
                i += 1                                                                                                  #Increment i by 1.
            Price = PriceRegex.group(i)                                                                                 #If we succeed, then our Price will be the regex group that we finished on.
        except AttributeError:                                                                                          #If we don't find anything in this regex:
            True                                                                                                        #Do nothing.
        Price = Price.replace("<span class=ITALIC>", "")                                                                #Filter out italic prices...
        Name = Name.replace("&amp", "&")                                                                                #Replace "&amp" with &
        Name = Name.replace("<span class=BOLD>","")                                                                     #Get rid of any Bold spannings
        Name = Name.replace("</span>","")                                                                             #Get rid of any ending tags.
        for char in DisallowedChars:                                                                                    #Check that our name doesn't have any blocked characters
            if char in Name:                                                                                            #Check it in the Name
                Name = Name.replace(char, "")                                                                           #Replace it with nothing
            if char in Price:                                                                                           #Check it in the Price
                Price = Price.replace(char, "")                                                                         #Replace it with nothing.

        print(f"Item: {Name}\n\tLink: {Link}\n\tPrice: {Price}\n")                                                      #Print to our screen the name, link, and price
        Output.write(f"{Name},{Price},{Link}\n")                                                                        #Print it to our CSV file
        OutputHTML.write(f"""
    <tr>
        <td>{Name}</td>
        <td>{Price}</td>
        <td class='ItemButton'>
            <button onclick='window.open(\"{Link}\")'>Link to Listing</button>
        </td>
    </tr>\n""")                                                                                                         #Print to our HTML file

        #Filter out our bad spans...
        
        #print(Items[i])
OutputHTML.write("</body></html>")#End our HTML file
Output.close();                                                                                                         #Close our CSV File
OutputHTML.close();                                                                                                     #Close our HTML File
OutputOption = input("Press [Enter] to open in a browser!")                                                             #Wait for user input
print(f"Current Operating System: {OSFind()}")                                                                          #Print the current OS
if OSFind() == "Linux":                                                                                                 #If Linux
    os.system("firefox Output.html")                                                                                    #Open in Firefox
elif OSFind() == "Windows":                                                                                             #If Windows
    edge = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe %s'                                            #Edge EXE Path
    webbrowser.get(edge).open(f"file://{os.getcwd()}/Output.html")                                                      #Open in Edge
elif OSFind() == "MacOS":                                                                                               #If MacOS
    webbrowser.get('safari').open(f"file://{os.getcwd()}/Output.html")                                                  #Open in Safari
