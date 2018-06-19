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

