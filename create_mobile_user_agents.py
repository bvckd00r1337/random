import random
import json

def generate_mobile_user_agents(count=1000):
    """Generate a diverse list of mobile user agents."""
    
    # Mobile device components
    devices = [
        # iOS devices
        "iPhone", "iPad", "iPod",
        # Samsung devices
        "SM-G998B", "SM-G996B", "SM-G991B", "SM-G980F", "SM-G970F", "SM-N986B", 
        "SM-N981B", "SM-N970F", "SM-A526B", "SM-A515F", "SM-A505F", "SM-A325F",
        # Additional Samsung devices
        "SM-A536B", "SM-S908B", "SM-S901B", "SM-F926B", "SM-F711B", "SM-A736B",
        "SM-A225F", "SM-A135F", "SM-M336B", "SM-M526B", "SM-A035F", "SM-F936B",
        "SM-G990B", "SM-A546B", "SM-A236B", "SM-A127F", "SM-A037G", "SM-A336B",
        # Google devices
        "Pixel 6", "Pixel 6 Pro", "Pixel 5", "Pixel 4a", "Pixel 4 XL", "Pixel 4",
        "Pixel 3a", "Pixel 3 XL", "Pixel 3",
        # New Google devices
        "Pixel 7", "Pixel 7 Pro", "Pixel 7a", "Pixel Fold", "Pixel Tablet",
        # OnePlus devices
        "OnePlus 9 Pro", "OnePlus 9", "OnePlus 8T", "OnePlus 8 Pro", "OnePlus 8",
        "OnePlus 7T Pro", "OnePlus 7T", "OnePlus 7 Pro", "OnePlus 7",
        # Additional OnePlus devices
        "OnePlus 10 Pro", "OnePlus 10T", "OnePlus Nord 2", "OnePlus Nord CE 2",
        "OnePlus 11", "OnePlus Nord 3", "OnePlus Nord CE 3", "OnePlus Pad",
        # Xiaomi devices
        "Mi 11", "Mi 10", "Redmi Note 10 Pro", "Redmi Note 10", "Redmi Note 9 Pro",
        "Redmi Note 9", "Redmi 9", "POCO F3", "POCO X3 Pro", "POCO X3",
        # Additional Xiaomi devices
        "Mi 12", "Mi 12 Pro", "Mi 12T", "Mi 12T Pro", "Redmi Note 11", "Redmi Note 11 Pro",
        "Redmi Note 12", "Redmi Note 12 Pro", "POCO F4", "POCO F4 GT", "POCO X4 GT",
        "POCO X5", "POCO X5 Pro", "Redmi 10", "Redmi 10C", "Redmi A1", "Xiaomi 12", "Xiaomi 13",
        # Other devices
        "Moto G Power", "Moto G Stylus", "Nokia 7.2", "Sony Xperia 5 II", "Sony Xperia 1 II",
        "HUAWEI P40 Pro", "HUAWEI P40", "HUAWEI P30 Pro", "HUAWEI P30",
        # Additional other devices
        "Moto G82", "Moto G72", "Moto G62", "Moto G52", "Moto G42", "Moto G32", "Moto Edge 30",
        "Nokia X20", "Nokia G50", "Nokia G21", "Nokia G11", "Nokia C21 Plus",
        "Sony Xperia 1 IV", "Sony Xperia 5 IV", "Sony Xperia 10 IV",
        "OPPO Find X5 Pro", "OPPO Find X5", "OPPO Reno 8 Pro", "OPPO Reno 8", "OPPO A77",
        "OPPO A57", "OPPO A17", "Realme GT 2 Pro", "Realme GT Neo 3", "Realme 9 Pro+",
        "Realme 9", "Realme C35", "Realme C33", "vivo X80 Pro", "vivo X80", "vivo V25 Pro",
        "vivo V25", "vivo Y22", "vivo Y35", "vivo Y55", "Nothing Phone 1"
    ]
    
    # iOS versions
    ios_versions = ["14_0", "14_1", "14_2", "14_3", "14_4", "14_5", "14_6", "14_7", "14_8",
                    "15_0", "15_1", "15_2", "15_3", "15_4", "15_5", "16_0", "16_1", "16_2", "16_3",
                    "16_4", "16_5", "16_6", "17_0", "17_1"]
    
    # Android versions
    android_versions = ["10", "11", "12", "12.1", "13", "14"]
    
    # Chrome versions for Android
    chrome_versions = [
        "91.0.4472.120", "92.0.4515.159", "93.0.4577.82", "94.0.4606.85", "95.0.4638.74",
        "96.0.4664.104", "97.0.4692.87", "98.0.4758.101", "99.0.4844.73", "100.0.4896.79",
        "101.0.4951.61", "102.0.5005.78", "103.0.5060.71", "104.0.5112.69", "105.0.5195.79",
        "106.0.5249.65", "107.0.5304.105", "108.0.5359.128", "109.0.5414.85", "110.0.5481.77",
        "111.0.5563.57", "112.0.5615.48", "113.0.5672.76", "114.0.5735.90",
        "115.0.5790.136", "116.0.5845.61", "117.0.5938.60", "118.0.5993.65", "119.0.6045.66",
        "120.0.6099.115", "121.0.6167.143", "122.0.6261.64", "123.0.6312.40"
    ]
    
    # Safari versions for iOS
    safari_versions = ["604.1", "605.1.15", "605.2.10", "605.3.8", "605.4.6", "605.5.7",
                      "605.6.3", "605.7.8", "605.8.4", "605.9.2", "605.10.3", "605.11.1",
                      "605.12.4", "605.13.7", "605.14.10", "605.15.13", "605.16.4",
                      "605.17.2", "605.18.1", "605.19.8", "605.20.6", "606.1.9", "606.2.3"]
    
    # Mobile Firefox versions
    firefox_versions = ["109.0", "110.0", "111.0", "112.0", "113.0", "114.0", "115.0", "116.0",
                       "117.0", "118.0", "119.0", "120.0", "121.0"]
    
    # Mobile Edge versions
    edge_versions = ["100.0.1185.50", "101.0.1210.53", "102.0.1245.44", "103.0.1264.71",
                    "104.0.1293.70", "105.0.1343.53", "106.0.1370.59", "107.0.1418.62",
                    "108.0.1462.76", "109.0.1518.78", "110.0.1587.69", "111.0.1661.62"]
    
    # Samsung Browser versions
    samsung_browser_versions = ["17.0", "18.0", "19.0", "20.0", "21.0", "22.0"]
    
    user_agents = []
    
    for _ in range(count):
        # Decide which browser type to generate
        browser_type = random.choices(
            ["iOS Safari", "Android Chrome", "Android Firefox", "Android Edge", "Samsung Browser"],
            weights=[35, 45, 10, 5, 5],
            k=1
        )[0]
        
        if browser_type == "iOS Safari":
            # iOS user agent
            device = random.choice(["iPhone", "iPad", "iPod"])
            ios_version = random.choice(ios_versions)
            safari_version = random.choice(safari_versions)
            
            # Fix the iOS version format in model string
            model = f"CPU {device} OS {ios_version.replace('_', ' ')} like Mac OS X"
            
            ua = f"Mozilla/5.0 ({model}) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/{safari_version}"
            user_agents.append(ua)
        
        elif browser_type == "Android Chrome":
            # Android Chrome user agent
            device = random.choice([d for d in devices if d not in ["iPhone", "iPad", "iPod"]])
            android_version = random.choice(android_versions)
            chrome_version = random.choice(chrome_versions)
            
            ua = f"Mozilla/5.0 (Linux; Android {android_version}; {device}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_version} Mobile Safari/537.36"
            user_agents.append(ua)
        
        elif browser_type == "Android Firefox":
            # Android Firefox user agent
            device = random.choice([d for d in devices if d not in ["iPhone", "iPad", "iPod"]])
            android_version = random.choice(android_versions)
            firefox_version = random.choice(firefox_versions)
            
            ua = f"Mozilla/5.0 (Android {android_version}; Mobile; rv:{firefox_version}) Gecko/{firefox_version} Firefox/{firefox_version}"
            user_agents.append(ua)
        
        elif browser_type == "Android Edge":
            # Android Edge user agent
            device = random.choice([d for d in devices if d not in ["iPhone", "iPad", "iPod"]])
            android_version = random.choice(android_versions)
            edge_version = random.choice(edge_versions)
            
            ua = f"Mozilla/5.0 (Linux; Android {android_version}; {device}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{edge_version.split('.')[0]}.0.0.0 Mobile Safari/537.36 EdgA/{edge_version}"
            user_agents.append(ua)
        
        else:  # Samsung Browser
            # Samsung Browser user agent (only for Samsung devices)
            samsung_devices = [d for d in devices if d.startswith("SM-")]
            device = random.choice(samsung_devices)
            android_version = random.choice(android_versions)
            chrome_base = random.choice(chrome_versions)
            samsung_version = random.choice(samsung_browser_versions)
            
            ua = f"Mozilla/5.0 (Linux; Android {android_version}; {device}) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/{samsung_version} Chrome/{chrome_base} Mobile Safari/537.36"
            user_agents.append(ua)
    
    # Ensure no duplicates
    return list(set(user_agents))

def save_user_agents(user_agents, filename="user_agents.txt"):
    """Save the generated user agents to a file."""
    with open(filename, "w") as file:
        for ua in user_agents:
            file.write(ua + "\n")
    print(f"Saved {len(user_agents)} mobile user agents to {filename}")

if __name__ == "__main__":
    # Number of user agents to generate
    count = 1000
    
    # Generate user agents
    user_agents = generate_mobile_user_agents(count)
    
    # Print a sample of 5 random user agents
    print("Sample of generated user agents:")
    for ua in random.sample(user_agents, min(5, len(user_agents))):
        print(f"- {ua}")
    
    # Save to file
    save_user_agents(user_agents)
    
    # Optionally save as JSON as well
    with open("user_agents.json", "w") as json_file:
        json.dump(user_agents, json_file, indent=2)
    print(f"Also saved user agents in JSON format to user_agents.json") 