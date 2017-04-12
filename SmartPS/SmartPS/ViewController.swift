//
//  ViewController.swift
//  SmartPS
//
//  Created by Princess Lyons on 3/26/17.
//  Copyright © 2017 Princess Lyons. All rights reserved.
//

import UIKit

class ViewController: UIViewController {
    
//    static let sharedInstance = ViewController()
    
    //  1. OPEN AND CLOSE CONNECTION IN AppDelegate.swift!!!
    //  2. RECEIVE DATA! - maybe create a simple label and try changing the text
    //  3. Handle when the app exits -> close the port/socket
    //  4. Fix switch funtionality
    //  5. Add UI for displaying costs and such...
    
    @IBOutlet weak var outletSwitch1: UISwitch!
    @IBOutlet weak var outletSwitch2: UISwitch!
    @IBOutlet weak var outletSwitch3: UISwitch!
    @IBOutlet weak var outletSwitch4: UISwitch!
    @IBOutlet weak var outletLabel1: UILabel!
    @IBOutlet weak var outletLabel2: UILabel!
    @IBOutlet weak var outletLabel3: UILabel!
    @IBOutlet weak var outletLabel4: UILabel!
    @IBOutlet weak var avgPower: UILabel!
    @IBOutlet weak var energyUsage: UILabel!
    @IBOutlet weak var cost: UILabel!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        print("Loaded")
        // Do any additional setup after loading the view, typically from a nib.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    @IBAction func outlet1(_ sender: Any) {
        //Code to turn off led
        
        //Fix functionality of switch. Only send message when switching on
        
        if outletSwitch1.isOn {
            SocketManager.sharedInstance.sendMessage(message: "LED1:on")
        }
        else {
            SocketManager.sharedInstance.sendMessage(message: "LED1:off")
        }
        
        //displayUsage()
    }

    @IBAction func outlet2(_ sender: Any) {
        //Code to turn off led
        
        if outletSwitch2.isOn {
            SocketManager.sharedInstance.sendMessage(message: "LED2:on")
        }
        else {
            SocketManager.sharedInstance.sendMessage(message: "LED2:off")
        }
    }
    
    @IBAction func outlet3(_ sender: Any) {
        //Code to turn off led
        
        if outletSwitch3.isOn {
            SocketManager.sharedInstance.sendMessage(message: "LED3:on")
        }
        else {
            SocketManager.sharedInstance.sendMessage(message: "LED3:off")
        }
    }
    
    @IBAction func outlet4(_ sender: Any) {
        //Code to turn off led
        
        if outletSwitch4.isOn {
            SocketManager.sharedInstance.sendMessage(message: "LED4:on")
        }
        else {
            SocketManager.sharedInstance.sendMessage(message: "LED4:off")
        }
    }
    
    func displayUsage() {
        while true {
            var value: String
            value = SocketManager.sharedInstance.readMessage()
            avgPower.text = value
            energyUsage.text = value
            cost.text = value
            print("Update values")
        }
    }
}
//Code to UI (Outlet) - like changing a label or something
//From UI to Code (Action)

