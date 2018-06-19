//
//  NotHotDog.swift
//  CognitiveServices
//
//  Created by Perry Shalom on 18/06/2018.
//  Copyright © 2018 Perry Sh. All rights reserved.
//

import UIKit
import MobileCoreServices

class NotHotDogViewController: CSViewController {
    @IBOutlet weak var btnPickImage: UIButton!
    var imagePickerController: UIImagePickerController!
    
    lazy var lblMissingCameraIndicator: UILabel = {
        let missingCameraIndicatorLabel = UILabel(frame: CGRect(x: 0, y: 0, width: 200, height: 200))
        missingCameraIndicatorLabel.text = "Missing camera!\nCan't recognize anything"
        missingCameraIndicatorLabel.textColor = UIColor.red.withAlphaComponent(0.8)
        missingCameraIndicatorLabel.textAlignment = .center
        missingCameraIndicatorLabel.numberOfLines = 0
        missingCameraIndicatorLabel.rotated(byRadians: -0.5)
        missingCameraIndicatorLabel.font = missingCameraIndicatorLabel.font.resized(size: 20)
        view.addSubview(missingCameraIndicatorLabel)
        missingCameraIndicatorLabel.matchConstraints(toView: btnPickImage)
        missingCameraIndicatorLabel.isPresented = false

        return missingCameraIndicatorLabel
    }()
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        imagePickerController = UIImagePickerController()
        imagePickerController.delegate = self
        
        guard isCameraAvailable else {
            print("This device has bo camera 😱")
            lblMissingCameraIndicator.isPresented = true
            btnPickImage.isEnabled = false
            return
        }
        
        imagePickerController.sourceType = UIImagePickerControllerSourceType.camera
        imagePickerController.mediaTypes = [kUTTypeImage.asString]
    }
    
    @IBAction func onPickImageButtonClicked(_ sender: UIButton) {
        guard isCameraAvailable else { return }
        present(imagePickerController, animated: true, completion: nil)
    }
    
    var isCameraAvailable: Bool {
        return UIImagePickerController.isSourceTypeAvailable(UIImagePickerControllerSourceType.camera)
    }
    
}

extension NotHotDogViewController: UIImagePickerControllerDelegate, UINavigationControllerDelegate {
    func imagePickerController(_ picker: UIImagePickerController, didFinishPickingMediaWithInfo info: [String : Any]) {
        
        let mediaUrl = info[UIImagePickerControllerReferenceURL].debugDescription
        print("picked image, location on disk: \(mediaUrl)")
        
        if let pickedMediaType = info[UIImagePickerControllerMediaType] {
            print("Picked a \(pickedMediaType)")
        }
        
        if let image = info[UIImagePickerControllerOriginalImage] as? UIImage {
            btnPickImage.setImage(image, for: .normal)
        }
        
        picker.dismiss(animated: true, completion: nil)
    }
}

