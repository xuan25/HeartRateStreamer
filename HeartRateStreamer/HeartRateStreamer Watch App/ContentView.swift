//
//  ContentView.swift
//  HeartRateStreamer Watch App
//
//  Created by Xuan25 on 07/10/2024.
//

import SwiftUI
import WatchKit
import Network

struct ContentView: View {
    // Use @ObservedObject to observe HeartRateManager in order to update the UI.
    @ObservedObject var heartRateManager = HeartRateManager.shared
    @ObservedObject var alertManager = AlertManager.shared
    @State private var serverAddr = ""
    
    var body: some View {
        VStack {
            Text("\(Image(systemName: "applewatch.case.inset.filled")) \(Image(systemName: "arrowshape.turn.up.forward")) \(Image(systemName: "desktopcomputer"))")
                .font(.headline)
                .padding(.bottom, 10)
                .padding(.top, 10)
            
            TextField("\(Image(systemName: "antenna.radiowaves.left.and.right")) ---.---.--.--:----", text: $serverAddr)
                .onSubmit() {
                    DataSender.shared.serverAddr = serverAddr;
                    UserDefaults.standard.setValue(serverAddr, forKey: "serverAddr")
                }
                .textInputAutocapitalization(.never)
                .disableAutocorrection(true)
                .padding(.bottom, 10)
            
            Text("\(Image(systemName: "heart.fill"))    \(heartRateManager.currentHeartRate >= 0 ? String(format: "%.0f", heartRateManager.currentHeartRate) : "\u{2012}\u{2012}\u{2012}")")
                    .font(.headline)
                    .padding(.bottom, 10)
            
            Button(action: {
                if heartRateManager.isActive {
                    // stop
                    heartRateManager.stopHeartRateCollection()
                } else {
                    // Save entered server address to UserDefaults
                    UserDefaults.standard.setValue(serverAddr, forKey: "serverIPAddress")
                    
                    // start
                    heartRateManager.startHeartRateCollection()
                }
            }) {
                if heartRateManager.isBusy {
                    ProgressView()
                } else {
                    Image(systemName: heartRateManager.isActive ? "stop.fill" : "play.fill")
                        .font(.title2)
                }
            }.background(heartRateManager.isActive ? Color.red : Color.green).cornerRadius(22)
            .disabled(heartRateManager.isBusy)
            .padding(.bottom, 10)
        }
        .padding()
        .onAppear {
            // Read previously stored server address from UserDefaults
            if let savedServerAddr = UserDefaults.standard.string(forKey: "serverAddr") {
                serverAddr = savedServerAddr
                DataSender.shared.serverAddr = serverAddr;
            }
        }.alert(isPresented: $alertManager.isShowing) {
            Alert(
                title: Text(alertManager.title),
                message: Text(alertManager.message)
            )
        }
    }
}

#Preview {
    ContentView()
}
