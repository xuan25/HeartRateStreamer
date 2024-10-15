//
//  DataSender.swift
//  HeartRateStreamer Watch App
//
//  Created by Xuan25 on 14/10/2024.
//

import Foundation

class DataSender {
    
    static let shared = DataSender()
    
    // Use @Published property to expose server address
    @Published var serverAddr: String = ""
    
    func sendHeartRateDataToServer(heartRate: Double) {
        
        guard !serverAddr.isEmpty else {
            print("No server IP address specified")
            return
        }
        
        let url = URL(string: "http://\(serverAddr)/heart-rate-endpoint")!
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        
        // Create json data to be sent
        let jsonData: [String: Any] = ["heartRate": heartRate, "timestamp": Date().timeIntervalSince1970]
        request.httpBody = try? JSONSerialization.data(withJSONObject: jsonData)
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        // Create URLSession data task
        let task = URLSession.shared.dataTask(with: request) { data, response, error in
            if let error = error {
                print("Failed to send heart rate data: \(error.localizedDescription)")
                return
            }
            
            if let httpResponse = response as? HTTPURLResponse, httpResponse.statusCode == 200 {
                print("Heart rate data sent successfully.")
            } else {
                print("Failed to send heart rate data, server error. code: \(String(describing: (response as? HTTPURLResponse)?.statusCode))")
            }
        }
        
        // Start the task
        task.resume()
    }
}
