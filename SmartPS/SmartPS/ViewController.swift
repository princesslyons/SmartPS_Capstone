//
//  ViewController.swift
//  SmartPS
//
//  Created by Princess Lyons on 3/26/17.
//  Copyright © 2017 Princess Lyons. All rights reserved.
//

import UIKit

class ViewController: UIViewController {
    
    //  1. OPEN AND CLOSE CONNECTION IN AppDelegate.swift!!!
    //  2. RECEIVE DATA! - maybe create a simple label and try changing the text
    //  3. Handle when the app exits -> close the port/socket
    //  4. Fix switch funtionality
    //  5. Add UI for displaying costs and such...
    
    
    override func viewDidLoad() {
        super.viewDidLoad()
        print("Loaded")
        //SocketManager.sharedInstance.NetworkEnable()
        // Do any additional setup after loading the view, typically from a nib.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    @IBAction func outlet1(_ sender: Any) {
        //Code to turn off led
        
        //Fix functionality of switch. Only send message when switching on
        
        //if switching on
        SocketManager.sharedInstance.sendMessage(message: "LED1:on")
        
        //if switching off
        //SocketManager.sharedInstance.sendMessage(message: "LED1:off")
    }

    @IBAction func outlet2(_ sender: Any) {
        //Code to turn off led
        
        //if switching on
        //SocketManager.sharedInstance.sendMessage(message: "LED2:on")
        
        SocketManager.sharedInstance.readMessage()
        
        
        //if switching off
        //SocketManager.sharedInstance.sendMessage(message: "LED2:off")
    }
    
    @IBAction func outlet3(_ sender: Any) {
        //Code to turn off led
        
        //if switching on
        SocketManager.sharedInstance.sendMessage(message: "LED3:on")
        
        //if switching off
        //SocketManager.sharedInstance.sendMessage(message: "LED3:off")
        
    }
    
    @IBAction func outlet4(_ sender: Any) {
        //Code to turn off led
        
        //if switching on
        SocketManager.sharedInstance.sendMessage(message: "QUIT")    //"LED4:on" - real message
        
        //if switching off
        //SocketManager.sharedInstance.sendMessage(message: "LED4:off")
    }
    
}
//Code to UI (Outlet) - like changing a label or something
//From UI to Code (Action)

