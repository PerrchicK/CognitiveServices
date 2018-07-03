//
//  CSViewController.swift
//  CognitiveServices
//
//  Created by Perry Shalom on 15/06/2018.
//  Copyright © 2018 Perry Sh. All rights reserved.
//

import UIKit

class Utilities { }

extension CFString {
    var asString: String {
        return self as String
    }
}

extension UIViewController {
    class func instantiate(storyboardName: String? = nil) -> Self {
        return instantiateFromStoryboardHelper(storyboardName)
    }
    
    fileprivate class func instantiateFromStoryboardHelper<T: UIViewController>(_ storyboardName: String?) -> T {
        let storyboard = storyboardName != nil ? UIStoryboard(name: storyboardName!, bundle: nil) : UIStoryboard(name: "Main", bundle: nil)
        let identifier = NSStringFromClass(T.self).components(separatedBy: ".").last!
        let controller = storyboard.instantiateViewController(withIdentifier: identifier) as! T
        return controller
    }
    
    func mostTopViewController() -> UIViewController {
        guard let topController = self.presentedViewController else { return self }
        
        return topController.mostTopViewController()
    }
}

extension UIAlertController {
    
    /**
     Dismisses the current alert (if presented) and pops up the new one
     */
    @discardableResult
    func show(completion: (() -> Swift.Void)? = nil) -> UIAlertController? {
        guard let mostTopViewController = UIApplication.mostTopViewController() else { print("Failed to present alert [title: \(String(describing: self.title)), message: \(String(describing: self.message))]"); return nil }
        
        mostTopViewController.present(self, animated: true, completion: completion)
        
        return self
    }
    
    func withAction(_ action: UIAlertAction) -> UIAlertController {
        self.addAction(action)
        return self
    }
    
    func withInputText(configurationBlock: @escaping ((_ textField: UITextField) -> Void)) -> UIAlertController {
        self.addTextField(configurationHandler: { (textField: UITextField!) -> () in
            configurationBlock(textField)
        })
        
        return self
    }
    
    static func make(style: UIAlertControllerStyle, title: String, message: String?) -> UIAlertController {
        let alertController = UIAlertController(title: title, message: message, preferredStyle: style)
        return alertController
    }
    
    static func makeActionSheet(title: String, message: String?) -> UIAlertController {
        return make(style: .actionSheet, title: title, message: message)
    }
    
    static func makeAlert(title: String, message: String) -> UIAlertController {
        return make(style: .alert, title: title, message: message)
    }
    
    /**
     A service method that alerts with title and message in the top view controller
     
     - parameter title: The title of the UIAlertView
     - parameter message: The message inside the UIAlertView
     */
    static func alert(title: String, message: String, dismissButtonTitle:String = "OK", onGone: (() -> Void)? = nil) {
        UIAlertController.makeAlert(title: title, message: message).withAction(UIAlertAction(title: dismissButtonTitle, style: UIAlertActionStyle.cancel, handler: { (alertAction) -> Void in
            onGone?()
        })).show()
    }
}

extension UIApplication {
    static func mostTopViewController() -> UIViewController? {
        guard let topController = UIApplication.shared.keyWindow?.rootViewController else { return nil }
        return topController.mostTopViewController()
    }
}

extension UIView {
    
    // MARK: - Helpers
    
    var isPresented: Bool {
        get {
            return !isHidden
        }
        set {
            isHidden = !newValue
        }
    }
    
    // MARK: - Constraints methods
    
    func matchConstraints(toView view: UIView, withInsets insets: UIEdgeInsets = UIEdgeInsets.zero) {
        let leftConstraint = constraintWithItem(view, attribute: .left, multiplier: 1, constant: insets.left)
        let topConstraint = constraintWithItem(view, attribute: .top, multiplier: 1, constant: insets.top)
        let rightConstraint = constraintWithItem(view, attribute: .right, multiplier: 1, constant: insets.right)
        let bottomConstraint = constraintWithItem(view, attribute: .bottom, multiplier: 1, constant: insets.bottom)
        
        let edgeConstraints = [leftConstraint, rightConstraint, topConstraint, bottomConstraint]
        
        translatesAutoresizingMaskIntoConstraints = false
        
        view.superview?.addConstraints(edgeConstraints)
    }
    
    func constraintWithItem(_ view: UIView, attribute: NSLayoutAttribute, multiplier: CGFloat, constant: CGFloat) -> NSLayoutConstraint {
        return NSLayoutConstraint(item: self, attribute: attribute, relatedBy: .equal, toItem: view, attribute: attribute, multiplier: multiplier, constant: constant)
    }
    
    func rotated(byRadians radians: CGFloat) {
        transform = transform.rotated(by: radians)
    }
    
}

extension UIFont {
    func resized(size: CGFloat) -> UIFont {
        return UIFont(descriptor: self.fontDescriptor, size: size)
    }
}

