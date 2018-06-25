//
//  SplashViewController.swift
//  CognitiveServices
//
//  Created by Perry Shalom on 15/06/2018.
//  Copyright © 2018 Perry Sh. All rights reserved.
//

import UIKit

class SplashViewController: CSViewController {
    override func viewDidAppear(_ animated: Bool) {
        super.viewDidAppear(animated)

        let seconds: Double = 0.5
        let delayTime = DispatchTime.now() + Double(Int64(seconds * Double(NSEC_PER_SEC))) / Double(NSEC_PER_SEC)
        DispatchQueue.main.asyncAfter(deadline: delayTime, execute: { [unowned self] in
            let vc = ImageOperationsViewController.instantiate()
            vc.modalTransitionStyle = .crossDissolve
            let navigationController = UINavigationController(rootViewController: vc)
            navigationController.isNavigationBarHidden = true
            self.present(navigationController, animated: true, completion: nil)
        })
    }
}
