import time
import random
import csv
import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException

class LinktreeClicker:
    def __init__(self, urls_file, proxies_file, user_agents_file, cycles=950):
        # Load data from files
        self.urls = self.load_list_from_file(urls_file)
        self.proxies = self.load_list_from_file(proxies_file)
        self.user_agents = self.load_list_from_file(user_agents_file)
        
        # Configuration
        self.wait_time = 3         # Increased wait time for page load
        self.visit_duration = 2    # Increased time to stay on each clicked link
        self.redirect_wait_time = 8  # Longer wait time for redirects
        self.cycles_per_url = cycles  # Number of cycles to run for each URL
        
        # Tracking
        self.cycle_counts = {url: 0 for url in self.urls}
        
        # Create data directory for tracking
        os.makedirs("data", exist_ok=True)
        
        # Load existing cycle counts if available
        self.load_cycle_counts()
        
        print(f"Loaded {len(self.urls)} URLs, {len(self.proxies)} proxies, and {len(self.user_agents)} user agents")
        print(f"Will run {self.cycles_per_url} cycles for each URL")
    
    def load_cycle_counts(self):
        """Load existing cycle counts from file if it exists"""
        try:
            if os.path.exists("data/cycle_counts.csv"):
                with open("data/cycle_counts.csv", 'r') as file:
                    reader = csv.reader(file)
                    for row in reader:
                        if len(row) == 2:
                            url, count = row
                            if url in self.cycle_counts:
                                self.cycle_counts[url] = int(count)
                print(f"Loaded existing cycle counts")
                for url, count in self.cycle_counts.items():
                    print(f"  {url}: {count}/{self.cycles_per_url} cycles completed")
        except Exception as e:
            print(f"Error loading cycle counts: {e}")
    
    def save_cycle_counts(self):
        """Save current cycle counts to file"""
        try:
            with open("data/cycle_counts.csv", 'w', newline='') as file:
                writer = csv.writer(file)
                for url, count in self.cycle_counts.items():
                    writer.writerow([url, count])
            print(f"Saved cycle counts to data/cycle_counts.csv")
        except Exception as e:
            print(f"Error saving cycle counts: {e}")
    
    def load_list_from_file(self, filename):
        """Load a list of items from a file (one item per line)"""
        try:
            with open(filename, 'r') as file:
                if filename.endswith('.csv'):
                    return [row[0] for row in csv.reader(file) if row]
                else:
                    return [line.strip() for line in file if line.strip()]
        except Exception as e:
            print(f"Error loading {filename}: {e}")
            return []
    
    def get_random_proxy(self):
        """Get a random proxy from the list"""
        if not self.proxies:
            return None
        return random.choice(self.proxies)
    
    def get_random_user_agent(self):
        """Get a random user agent from the list"""
        if not self.user_agents:
            return "Mozilla/5.0 (Linux; Android 10; SM-G970F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36"
        return random.choice(self.user_agents)
    
    def create_driver(self, proxy=None, user_agent=None):
        """Create a new Firefox WebDriver instance with the given proxy and user agent"""
        options = Options()
        options.headless = False  # Set to True for headless mode
        
        # Speed optimization settings but less aggressive
        options.set_preference("permissions.default.image", 2)  # Block images
        options.set_preference("browser.cache.disk.enable", False)
        
        # Handle protocol errors more gracefully
        options.set_preference("browser.xul.error_pages.enabled", True)
        options.set_preference("browser.tabs.warnOnClose", False)
        
        # Handle problematic URLs better
        options.set_preference("browser.fixup.alternate.enabled", False)  # Don't try to "fix" URLs
        options.set_preference("browser.urlbar.trimURLs", False)  # Don't trim URLs
        options.set_preference("network.standard-url.enable-rust", False)  # Use legacy URL parser
        
        if user_agent:
            options.set_preference("general.useragent.override", user_agent)
        
        if proxy:
            # Format: "host:port"
            parts = proxy.split(':')
            if len(parts) == 2:
                host, port = parts
                options.set_preference("network.proxy.type", 1)
                options.set_preference("network.proxy.http", host)
                options.set_preference("network.proxy.http_port", int(port))
                options.set_preference("network.proxy.ssl", host)
                options.set_preference("network.proxy.ssl_port", int(port))
        
        driver = webdriver.Firefox(options=options)
        driver.set_page_load_timeout(30)  # Increased timeout for better reliability
        return driver
    
    def handle_protocol_error(self, driver, url):
        """Handle various protocol errors gracefully"""
        try:
            current_url = driver.current_url
            
            # Check for about:neterror pages
            if "about:neterror" in current_url:
                error_message = ""
                try:
                    # Try to get the error message from the page
                    error_message = driver.find_element(By.CSS_SELECTOR, ".title").text
                except:
                    pass
                
                # Handle "The address wasn't understood" error
                if "address wasn't understood" in error_message or "wasn't understood" in current_url:
                    print("  ✓ Address format error - normal for app deep links, counting as success")
                    time.sleep(self.visit_duration)
                    return True
                    
                # Handle unknownProtocolFound error 
                if "unknownProtocolFound" in current_url:
                    print("  ✓ App deep link detected - counting as success")
                    time.sleep(self.visit_duration)
                    return True
            
            # Check for URLs that might cause issues
            if "adj.st" in url and "adjust_t=" in url:
                # This is likely an Adjust tracking URL that will deep link to an app
                print("  ✓ Adjust tracking URL detected - counting as success")
                time.sleep(self.visit_duration)
                return True
                
        except Exception as e:
            print(f"  Error in protocol error handling: {e}")
        
        return False
    
    def wait_for_redirect(self, driver, original_url):
        """Wait for a redirect to complete and then wait 1 second"""
        start_time = time.time()
        
        try:
            # Brief initial wait for redirect to start
            time.sleep(1)
            
            # Pre-check for problematic URLs that we know will cause issues
            if "adj.st" in original_url:
                print(f"  Adjust tracking URL detected: {original_url[:50]}...")
                
                # These often lead to deep links or app stores
                # Try to get as far as possible in the redirect chain
                try:
                    # Wait for any initial redirect
                    time.sleep(2)
                    
                    # Check current state
                    if self.handle_protocol_error(driver, original_url):
                        return True
                    
                    # Check if URL changed
                    current_url = driver.current_url
                    if current_url != original_url:
                        print(f"  First redirect to: {current_url[:50]}...")
                        time.sleep(1)
                        return True
                except:
                    # Handle any errors as success for adjust URLs
                    print("  ✓ Adjust URL processing completed (with error)")
                    time.sleep(1)
                    return True
            
            # Check if there's a protocol error first
            if self.handle_protocol_error(driver, original_url):
                return True
            
            # Check if URL changed
            try:
                current_url = driver.current_url
                if current_url != original_url:
                    print(f"  Redirected to: {current_url[:50]}...")
                    
                    # Check for protocol error again
                    if self.handle_protocol_error(driver, original_url):
                        return True
                    
                    # Wait for page to stabilize
                    try:
                        WebDriverWait(driver, 3).until(
                            lambda d: d.execute_script('return document.readyState') == 'complete'
                        )
                    except:
                        pass
                    
                    # Wait exactly 1 second after redirect as requested
                    time.sleep(1)
                    return True
            except Exception as e:
                print(f"  Error checking redirect: {e}")
            
            # Monitor for a bit longer
            elapsed = 0
            while elapsed < self.redirect_wait_time:
                try:
                    # Check current URL
                    current_url = driver.current_url
                    
                    # Handle protocol errors
                    if self.handle_protocol_error(driver, original_url):
                        return True
                    
                    # Check if URL changed from original
                    if current_url != original_url and "about:blank" not in current_url:
                        print(f"  Redirect detected: {current_url[:50]}...")
                        time.sleep(1)  # Wait 1 second after redirect
                        return True
                except:
                    pass
                
                # Sleep a bit before checking again
                time.sleep(1)
                elapsed = time.time() - start_time
            
            # Default - wait 1 second anyway
            time.sleep(1)
            return False
            
        except Exception as e:
            print(f"  Error in redirect wait: {e}")
            # Wait 1 second anyway
            time.sleep(1)
            return False
    
    def process_linktree(self, url, proxy, user_agent):
        """
        Process a Linktree URL, extracting all links and visiting each one
        """
        driver = None
        try:
            print(f"\nProcessing: {url}")
            print(f"Using proxy: {proxy}")
            print(f"Using user agent: {user_agent[:50]}...")
            
            driver = self.create_driver(proxy, user_agent)
            
            # Visit the Linktree page
            driver.get(url)
            
            # Wait for the page to load
            WebDriverWait(driver, self.wait_time).until(
                EC.presence_of_element_located((By.TAG_NAME, "a"))
            )
            
            # Wait a bit longer for stability
            time.sleep(2)
            
            # EXTRACT ALL LINKS
            all_hrefs = []
            
            # Try specific selectors from Linktree
            selectors = [
                "a[href*='ty.gl']",                 # Your ty.gl links
                "a[data-testid='LinkButton']",      # LinkButton test ID
                "div[data-linktype='CLASSIC'] a"    # CLASSIC links
            ]
            
            # Collect all hrefs using various selectors
            for selector in selectors:
                try:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        href = element.get_attribute("href")
                        if href and "linktree" not in href and href not in all_hrefs:
                            all_hrefs.append(href)
                except:
                    continue
            
            # If no links found with specific selectors, try all links
            if not all_hrefs:
                try:
                    elements = driver.find_elements(By.TAG_NAME, "a")
                    for element in elements:
                        href = element.get_attribute("href")
                        if href and "linktree" not in href and href not in all_hrefs:
                            all_hrefs.append(href)
                except:
                    pass
            
            print(f"Found {len(all_hrefs)} unique links to process")
            
            # PROCESS EACH LINK
            for i, href in enumerate(all_hrefs):
                try:
                    print(f"  Processing link {i+1}/{len(all_hrefs)}: {href[:50]}...")
                    
                    # Open in new tab with error handling
                    try:
                        original_window = driver.current_window_handle
                        driver.switch_to.new_window('tab')
                        
                        # Navigate to the link with proper error handling
                        try:
                            # If we know this is potentially an adjustment URL that could fail
                            if "adj.st" in href:
                                try:
                                    driver.get(href)
                                    self.wait_for_redirect(driver, href)
                                except Exception as adjust_error:
                                    # For adj.st URLs, count any errors as success
                                    print(f"  ✓ Adjust URL processing completed (error: {adjust_error})")
                                    time.sleep(self.visit_duration)
                            else:
                                # Regular URL handling
                                driver.get(href)
                                self.wait_for_redirect(driver, href)
                        except Exception as e:
                            # Check error message for various conditions
                            error_str = str(e).lower()
                            if "address wasn't understood" in error_str or "unknownprotocol" in error_str:
                                print("  ✓ App deep link error detected - counting as success")
                                time.sleep(self.visit_duration)
                            else:
                                print(f"  Navigation error: {e}")
                        
                        # Close tab and switch back
                        driver.close()
                        driver.switch_to.window(original_window)
                    except Exception as tab_error:
                        print(f"  Error managing tab: {tab_error}")
                        # Recovery
                        try:
                            windows = driver.window_handles
                            if original_window in windows:
                                driver.switch_to.window(original_window)
                            elif windows:
                                driver.switch_to.window(windows[0])
                        except:
                            pass
                    
                except Exception as e:
                    print(f"  Error processing link: {e}")
                    # Make sure we're back on the main tab
                    try:
                        windows = driver.window_handles
                        if len(windows) > 0:
                            driver.switch_to.window(windows[0])
                    except:
                        pass
                
                # Slightly longer delay between links for stability
                time.sleep(random.uniform(1, 2))
            
            # Record this cycle
            self.cycle_counts[url] += 1
            print(f"Completed cycle {self.cycle_counts[url]}/{self.cycles_per_url} for {url}")
            
            # Save cycle counts after each full cycle
            self.save_cycle_counts()
            
            # Rest between cycles
            time.sleep(3)
            
            return True
            
        except Exception as e:
            print(f"Error processing Linktree: {e}")
            return False
        
        finally:
            if driver:
                driver.quit()
    
    def run(self):
        """Process all URLs for the specified number of cycles"""
        try:
            # Continue until all URLs have completed their cycles
            while True:
                # Check if all URLs have completed their cycles
                all_completed = True
                for url, count in self.cycle_counts.items():
                    if count < self.cycles_per_url:
                        all_completed = False
                        break
                
                if all_completed:
                    print("All URLs have completed their cycles!")
                    break
                
                # Process each URL that hasn't completed its cycles
                for url in self.urls:
                    if self.cycle_counts[url] < self.cycles_per_url:
                        # Get a new proxy and user agent for each cycle
                        proxy = self.get_random_proxy()
                        user_agent = self.get_random_user_agent()
                        
                        print(f"\n[URL {self.urls.index(url)+1}/{len(self.urls)}] Processing: {url}")
                        print(f"Cycle: {self.cycle_counts[url]+1}/{self.cycles_per_url}")
                        
                        try:
                            self.process_linktree(url, proxy, user_agent)
                        except Exception as e:
                            print(f"Error processing {url}: {e}")
                        
                        # Longer delay between URLs for stability
                        time.sleep(random.uniform(2, 3))
        
        except KeyboardInterrupt:
            print("\nScript interrupted by user. Saving progress...")
            self.save_cycle_counts()
            print("Progress saved. You can resume later.")
        
        except Exception as e:
            print(f"Unexpected error in main loop: {e}")
            self.save_cycle_counts()
        
        finally:
            # Always save cycle counts at the end
            self.save_cycle_counts()
            print("\nAll processing completed!")

if __name__ == "__main__":
    # File paths
    urls_file = "urls.txt"  # One URL per line
    proxies_file = "proxies.txt"  # One proxy per line in format host:port
    user_agents_file = "user_agents.txt"  # One user agent per line
    
    # Create and run the clicker with 950 cycles per URL
    clicker = LinktreeClicker(urls_file, proxies_file, user_agents_file, cycles=950)
    clicker.run() 