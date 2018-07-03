//
//  ServicesViewController.swift
//  CognitiveServices
//
//  Created by Perry Shalom on 15/06/2018.
//  Copyright © 2018 Perry Sh. All rights reserved.
//

import UIKit

class ServicesViewController: CSViewController {

    override func viewDidAppear(_ animated: Bool) {
        super.viewDidAppear(animated)

    }
    
    func callApi() {
        let urlString = String(format: "https://maps.googleapis.com/maps/api/geocode/json?latlng=%f,%f&key=%@", 0.0, 0.0 , apiKey)
        guard let url = URL(string: urlString) else { return }
        let request = URLRequest(url: url)
        
        let dataTask = URLSession.shared.dataTask(with: request, completionHandler: { [weak self] (data, response, connectionError) -> Void in
            guard let data = data else { return }
            if connectionError == nil {
                do {
                    let innerJson = try JSONSerialization.jsonObject(with: data, options: JSONSerialization.ReadingOptions.mutableContainers)
                    //let toastText = self?.parseResponse(innerJson) ?? "Parsing failed"
                    print(innerJson)
                    print("\(self)")
                } catch {
                    print("Error: (\(error))")
                }
            }
        })
        
        // Go fetch...
        dataTask.resume()
    }
}
