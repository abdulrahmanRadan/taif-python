import React, { useState } from "react";
import { View, Text, TextInput, TouchableOpacity, Alert } from "react-native";

const AddDebtScreen = ({ navigation }) => {
  const [debtName, setDebtName] = useState("");
  const [amount, setAmount] = useState("");

  const handleAddDebt = () => {
    if (!debtName || !amount) {
      Alert.alert("Error", "Please fill in all fields");
      return;
    }

    // Add debt logic (replace with actual logic to save the debt)
    console.log("Debt Added:", { debtName, amount });

    // Navigate back or show confirmation
    navigation.goBack();
  };

  return (
    <View className="flex-1 bg-white p-4">
      <Text className="text-xl font-bold mb-4">Add New Debt</Text>

      <Text className="mb-2 text-gray-700">Debt Name</Text>
      <TextInput
        className="border border-gray-300 p-2 rounded-lg mb-4"
        placeholder="Enter debt name"
        value={debtName}
        onChangeText={setDebtName}
      />

      <Text className="mb-2 text-gray-700">Amount</Text>
      <TextInput
        className="border border-gray-300 p-2 rounded-lg mb-4"
        placeholder="Enter amount"
        value={amount}
        onChangeText={setAmount}
        keyboardType="numeric"
      />

      <TouchableOpacity
        className="bg-blue-500 p-4 rounded-lg"
        onPress={handleAddDebt}
      >
        <Text className="text-white text-center font-bold">Add Debt</Text>
      </TouchableOpacity>
    </View>
  );
};

const EditDebtScreen = ({ route, navigation }) => {
  const { debtName: initialDebtName, amount: initialAmount } = route.params;
  const [debtName, setDebtName] = useState(initialDebtName);
  const [amount, setAmount] = useState(initialAmount);

  const handleEditDebt = () => {
    if (!debtName || !amount) {
      Alert.alert("Error", "Please fill in all fields");
      return;
    }

    // Edit debt logic (replace with actual logic to save changes)
    console.log("Debt Updated:", { debtName, amount });

    // Navigate back or show confirmation
    navigation.goBack();
  };

  return (
    <View className="flex-1 bg-white p-4">
      <Text className="text-xl font-bold mb-4">Edit Debt</Text>

      <Text className="mb-2 text-gray-700">Debt Name</Text>
      <TextInput
        className="border border-gray-300 p-2 rounded-lg mb-4"
        placeholder="Enter debt name"
        value={debtName}
        onChangeText={setDebtName}
      />

      <Text className="mb-2 text-gray-700">Amount</Text>
      <TextInput
        className="border border-gray-300 p-2 rounded-lg mb-4"
        placeholder="Enter amount"
        value={amount}
        onChangeText={setAmount}
        keyboardType="numeric"
      />

      <TouchableOpacity
        className="bg-green-500 p-4 rounded-lg"
        onPress={handleEditDebt}
      >
        <Text className="text-white text-center font-bold">Save Changes</Text>
      </TouchableOpacity>
    </View>
  );
};

export { AddDebtScreen, EditDebtScreen };
