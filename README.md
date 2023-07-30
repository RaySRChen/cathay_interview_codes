# README file for cath_bank_automation_test_for_Android.py

This automated test script is specifically designed for performing automated tests on the Chrome App with the Cathay Bank website. The script is written in Python and uses the Appium testing framework to simulate user interactions and execute test scenarios while recording the results. This README file provides a detailed explanation of the script, including its features, system requirements, installation instructions, and usage guidelines.

Features
This automated test script offers the following functionalities:

Question 1 Test: Opens the Cathay Bank website using the Chrome app and takes a screenshot of the webpage.
Question 2 Test: Navigates to Personal Finance > Product Introduction > Credit Card List and calculates the number of items under the credit card menu, taking a screenshot of the menu.
Question 3 Test: Navigates to Personal Finance > Product Introduction > Credit Card > Card Introduction, calculates the number of discontinued credit cards on the page, and takes screenshots of each.
System Requirements
Before running this automated test script, make sure your system meets the following requirements:

Android Device: Your device must support the Appium testing framework.
Python: Install Python 3.x on your system.
Appium Server: Install and run the Appium Server.
Installation
Download the Code: Download the latest version of the script from GitHub.

Install Dependencies: Use pip to install the required dependencies.

bash
Copy code
pip install appium-python-client
pip install selenium
Configure Appium Server: Ensure that the Appium Server settings match your Android device. Modify the appium_server, platform_version, device_name, app_package, and app_activity variables to reflect your test environment.
Usage
Run the Tests: Execute the script from the command line, and the script will automatically perform all the test scenarios.
bash
Copy code
python cathay_bank_automation_test_for_android.py
Test Results: The script will output the test results and save the screenshots to the specified files.

Logs: The test logs will be saved in the cathay_bank_automation_log.txt file.

Notes
Ensure that your Android device is connected to your computer and supports the Appium testing framework.
Before running the script, ensure that the Appium Server is running correctly and connected to the device.
Make sure the appium_server, platform_version, device_name, app_package, and app_activity variables are properly configured to match your test environment.
This script is designed for testing in a specific environment and configuration. If used in other environments, adjustments and modifications may be required.
Contribution
If you encounter any issues or have suggestions for improvements, please feel free to submit issues or pull requests. Your contributions are welcome to enhance this automated test script!

Contact
If you have any questions or need further assistance, please don't hesitate to contact us. Thank you for using and supporting this automated test script!

License
This automated test script is licensed under the MIT License. Please refer to the LICENSE file for more detailed information.
