//
//  HeartRateManager.swift
//  HeartRateStreamer Watch App
//
//  Created by Xuan25 on 07/10/2024.
//

import Foundation
import HealthKit

class HeartRateManager: NSObject, ObservableObject {
    static let shared = HeartRateManager()
    
    private let healthStore = HKHealthStore()
    private var workoutSession: HKWorkoutSession?
    private var workoutBuilder: HKLiveWorkoutBuilder?
    
    // Use @Published property to expose real-time heart rate data
    @Published var currentHeartRate: Double = -1;
    @Published var isActive: Bool = false;
    @Published var isBusy: Bool = false;
    
    func requestAuthorization(completionHandler: ((Bool) -> Void)?) {
        let typesToShare: Set<HKSampleType> = [
            HKObjectType.workoutType()
        ]
        let typesToRead: Set<HKObjectType> = [HKObjectType.quantityType(forIdentifier: .heartRate)!
        ]
        
        healthStore.requestAuthorization(toShare: typesToShare, read: typesToRead) { (success, error) in
            if success {
                print("Permission granted for heart rate data.")
            } else {
                if let error = error {
                    
                    AlertManager.shared.showMessage(title: "Error", message: "Permission denied with error: \(error.localizedDescription)")
                    print("Permission denied with error: \(error.localizedDescription)")
                } else {
                    AlertManager.shared.showMessage(title: "Error", message: "Permission denied for heart rate data.")
                    print("Permission denied for heart rate data.")
                }
            }
            completionHandler?(success)
        }
    }
    
    func startHeartRateCollection() {
        
        isBusy = true
        
        requestAuthorization(completionHandler: {
            (success) in
            if !success{
                DispatchQueue.main.async {
                    self.isBusy = false
                }
                return
            }
            
            let configuration = HKWorkoutConfiguration()
            configuration.activityType = .other
            configuration.locationType = .indoor
            
            do {
                self.workoutSession = try HKWorkoutSession(healthStore: self.healthStore, configuration: configuration)
                self.workoutBuilder = self.workoutSession?.associatedWorkoutBuilder()
                
                self.workoutBuilder?.dataSource = HKLiveWorkoutDataSource(healthStore: self.healthStore, workoutConfiguration: configuration)
                self.workoutSession?.delegate = self
                self.workoutBuilder?.delegate = self
                
                self.workoutSession?.startActivity(with: Date())
                self.workoutBuilder?.beginCollection(withStart: Date(), completion: { (success, error) in
                    if success {
                        print("workout session started")
                        DispatchQueue.main.async {
                            self.isActive = true
                            self.isBusy = false
                        }
                    } else if let error = error {
                        print("Error starting workout session: \(error.localizedDescription)")
                        AlertManager.shared.showMessage(title: "Error", message: "Error starting workout session: \(error.localizedDescription)")
                        DispatchQueue.main.async {
                            self.isBusy = false
                        }
                    }
                })
            } catch {
                print("Failed to start workout session: \(error.localizedDescription)")
                AlertManager.shared.showMessage(title: "Error", message: "Failed to start workout session: \(error.localizedDescription)")
                DispatchQueue.main.async {
                    self.isBusy = false
                }
                return
            }
        })
        
    }
    
    func stopHeartRateCollection() {
        
        isBusy = true
        
        workoutSession?.end()
        workoutBuilder?.endCollection(withEnd: Date(), completion: { (success, error) in
            if let error = error {
                print("Error stopping workout session: \(error.localizedDescription)")
                AlertManager.shared.showMessage(title: "Error", message: "Error stopping workout session: \(error.localizedDescription)")
                DispatchQueue.main.async {
                    self.isBusy = false
                }
                return
            }
            
            DispatchQueue.main.async {
                self.currentHeartRate = -1
                self.isBusy = false;
                self.isActive = false;
            }
        })
    }
}

extension HeartRateManager: HKWorkoutSessionDelegate, HKLiveWorkoutBuilderDelegate {
    
    func workoutBuilderDidCollectEvent(_ workoutBuilder: HKLiveWorkoutBuilder) {
        
    }
    
    func workoutBuilder(_ workoutBuilder: HKLiveWorkoutBuilder, didCollectDataOf collectedTypes: Set<HKSampleType>) {
        print("data collected")
        for type in collectedTypes {
            if type.identifier == HKQuantityTypeIdentifier.heartRate.rawValue {
                if let heartRateType = HKQuantityType.quantityType(forIdentifier: .heartRate),
                   let statistics = workoutBuilder.statistics(for: heartRateType) {
                    
                    let heartRateUnit = HKUnit.count().unitDivided(by: HKUnit.minute())
                    if let heartRate = statistics.mostRecentQuantity()?.doubleValue(for: heartRateUnit) {
                        
                        print("Collected Heart Rate: \(heartRate)")
                        
                        // update heart rate data in UI
                        DispatchQueue.main.async {
                            self.currentHeartRate = heartRate
                        }
                        
                        // send heart rate data to the server via HTTP
                        DataSender.shared.sendHeartRateDataToServer(heartRate: heartRate)
                        
                    } else {
                        print("Failed to retrieve heart rate quantity.")
                    }
                } else {
                    print("No statistics available for heart rate.")
                }
            }
        }
    }
    
    func workoutSession(_ workoutSession: HKWorkoutSession, didChangeTo toState: HKWorkoutSessionState, from fromState: HKWorkoutSessionState, date: Date) {
        // Handle state changes if needed
    }
    
    func workoutSession(_ workoutSession: HKWorkoutSession, didFailWithError error: Error) {
        print("Workout session failed: \(error.localizedDescription)")
        AlertManager.shared.showMessage(title: "Error", message: "Workout session failed: \(error.localizedDescription)")
        DispatchQueue.main.async {
            self.currentHeartRate = -1
            self.isActive = false;
        }
    }
}
