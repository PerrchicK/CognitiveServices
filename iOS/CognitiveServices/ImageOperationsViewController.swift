//
//  NotHotDog.swift
//  CognitiveServices
//
//  Created by Perry Shalom on 18/06/2018.
//  Copyright © 2018 Perry Sh. All rights reserved.
//

import UIKit
import MobileCoreServices
import OnGestureSwift

class ImageOperationsViewController: CSViewController {
    
    class Constants {
        static let PersonId_Perry = "d50a4f57-6c30-4c38-8bc8-b4368e41255d"
        static let PersonId_Nikolai = "6b2e3cdf-a5b7-456f-baf6-c104773955b4"
        static let PersonsGroupId = "meetup_persons_list"
    }

    @IBOutlet weak var btnPickImage: UIButton!
    @IBOutlet weak var lblStatus: UILabel!
    @IBOutlet weak var txtResponseBody: UITextView!
    @IBOutlet weak var lblResponseTitle: UILabel!
    @IBOutlet weak var imgPickedImage: UIImageView!

    var lastDetectedFaceId: String?

    lazy var imagePickerController: UIImagePickerController = {
        let imagePickerController = UIImagePickerController()
        imagePickerController.delegate = self
        
        guard isCameraAvailable else {
            print("This device has bo camera 😱")
            lblMissingCameraIndicator.isPresented = true
            btnPickImage.isEnabled = false
            return imagePickerController
        }
        
        imagePickerController.sourceType = UIImagePickerControllerSourceType.camera
        imagePickerController.mediaTypes = [kUTTypeImage.asString]

        return imagePickerController
    }()
    
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

        imgPickedImage.onClick { [unowned self] _ in
            self.pickImage()
        }

        btnPickImage.onClick { [unowned self] _ in
            self.pickImage()
        }
    }

    func pickImage() {
        guard isCameraAvailable else { return }

        UIAlertController.makeActionSheet(title: "Camera?", message: "This will open your device's camera")
            .withAction(UIAlertAction(title: "Oops...", style: UIAlertActionStyle.cancel, handler: nil))
            .withAction(UIAlertAction(title: "Capture Face(s)", style: UIAlertActionStyle.default, handler: { [unowned self] (alertAction) in
                self.present(self.imagePickerController, animated: true, completion: nil)
            })).show()
    }

    var isCameraAvailable: Bool {
        return UIImagePickerController.isSourceTypeAvailable(UIImagePickerControllerSourceType.camera)
    }
    
    func onImagePicked(image: UIImage) {
        imgPickedImage.image = image

        guard let imageData = UIImageJPEGRepresentation(image, 0.7) else { return }
        self.faceServiceClient.detect(with: imageData, returnFaceId: true, returnFaceLandmarks: true, returnFaceAttributes: nil) { [weak self] (faces, error) in
            if let error = error {
                print("Cognitive detection error: \(error)")
            } else {
                guard let faceId = faces?.last?.faceId else { return }
                self?.lastDetectedFaceId = faceId
                self?.lblStatus.text = "Done"
                self?.txtResponseBody.text = "Detection results: last face ID = \(faceId)"
            }
        }
    }

    @IBAction func onPerformActionClicked(_ sender: UIButton) {
        UIAlertController.makeActionSheet(title: "Choose an action", message: nil)
            .withAction(UIAlertAction(title: "Cancel", style: UIAlertActionStyle.cancel, handler: nil))
            .withAction(UIAlertAction(title: "Smiley faces counter", style: UIAlertActionStyle.default, handler: { [unowned self] (alertAction) in
                guard let image = self.imgPickedImage.image, let imageData = UIImageJPEGRepresentation(image, 0.7) else { return }
                self.faceServiceClient.detect(with: imageData, returnFaceId: false, returnFaceLandmarks: false, returnFaceAttributes: [MPOFaceAttributeTypeEmotion.rawValue]) { [weak self] (faces, error) in
                    if let error = error {
                        print("Cognitive detection error: \(error)")
                    } else if let faces = faces {
                        var smilesCounter: Int = 0
                        for face in faces {
                            if let smileValue = face.attributes?.smile?.doubleValue, smileValue > 0.5 {
                                smilesCounter += 1
                            } else if let isHappy = face.attributes?.emotion?.happiness?.boolValue, isHappy {
                                smilesCounter += 1
                            }
                        }
                        self?.lblStatus.text = "Done"
                        self?.txtResponseBody.text = "Detection results: smiles counter = \(smilesCounter)"
                    }
                }
            }))
            .withAction(UIAlertAction(title: "Create group", style: UIAlertActionStyle.default, handler: { [unowned self] (alertAction) in
                guard self.imgPickedImage.image != nil else { return }
            }))
            .withAction(UIAlertAction(title: "Add person", style: UIAlertActionStyle.default, handler: { [unowned self] (alertAction) in
                guard let faceId = self.lastDetectedFaceId else { return }
            }))
            .withAction(UIAlertAction(title: "Add face to person", style: UIAlertActionStyle.default, handler: { [unowned self] (alertAction) in
                guard let faceId = self.lastDetectedFaceId else { return }
            }))
            .withAction(UIAlertAction(title: "Train", style: UIAlertActionStyle.default, handler: { [unowned self] (alertAction) in
                guard let faceId = self.lastDetectedFaceId else { return }
            }))
            .withAction(UIAlertAction(title: "Verify", style: UIAlertActionStyle.default, handler: { [unowned self] (alertAction) in
                guard let faceId = self.lastDetectedFaceId, self.imgPickedImage.image != nil else { return }
                self.faceServiceClient.verify(withFaceId: faceId, personId: Constants.PersonId_Nikolai, personGroupId: Constants.PersonsGroupId, completionBlock: { [weak self] (verificationResult, error) in
                    if let error = error { print("Failed! Error: \(error)"); return }
                    guard let verificationResult = verificationResult, let confidence = verificationResult.confidence else { print("Failed to extract result!"); return }
                    
                    self?.txtResponseBody.text = "Verification results: is identical = \(verificationResult.isIdentical), confidence = \(confidence)"
                    self?.lblStatus.text = "Done"
                })
            }))
        .show()
    }
}

extension ImageOperationsViewController: UIImagePickerControllerDelegate, UINavigationControllerDelegate {
    func imagePickerController(_ picker: UIImagePickerController, didFinishPickingMediaWithInfo info: [String : Any]) {
        let mediaUrl = info[UIImagePickerControllerReferenceURL].debugDescription
        print("picked image, location on disk: \(mediaUrl)")
        
        if let pickedMediaType = info[UIImagePickerControllerMediaType] {
            print("Picked a \(pickedMediaType)")
        }
        
        if let image = info[UIImagePickerControllerOriginalImage] as? UIImage {
            onImagePicked(image: image)
        }
        
        picker.dismiss(animated: true, completion: nil)
    }
}
