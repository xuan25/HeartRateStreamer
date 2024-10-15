//
//  ViewModel.swift
//  HeartRateStreamer Watch App
//
//  Created by Xuan25 on 15/10/2024.
//

import Foundation

class AlertManager: NSObject, ObservableObject {
    static let shared = AlertManager()
    
    @Published var isShowing: Bool = false
    @Published var title: String = "Title"
    @Published var message: String = "message"
    
    func showMessage(title: String, message: String) {
        DispatchQueue.main.async {
            self.title = title
            self.message = message
            self.isShowing = true
        }
    }
}
