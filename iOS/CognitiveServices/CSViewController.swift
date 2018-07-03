//
//  Utilities.swift
//  CognitiveServices
//
//  Created by Perry Shalom on 15/06/2018.
//  Copyright © 2018 Perry Sh. All rights reserved.
//

import UIKit

/// CSViewController stands for: CognitiveServicesViewController
class CSViewController: UIViewController {
    lazy var apiKey: String = {
        let key = (UIApplication.shared.delegate as? AppDelegate)?.constantStrings?["FaceSubscriptionKey"] as? String
        
        return key ?? ""
    }()

    lazy var faceServiceClient: MPOFaceServiceClient = {
        let ProjectOxfordFaceEndpoint = "https://westeurope.api.cognitive.microsoft.com/face/v1.0/"
        return MPOFaceServiceClient(endpointAndSubscriptionKey: ProjectOxfordFaceEndpoint, key: apiKey)
    }()
}
