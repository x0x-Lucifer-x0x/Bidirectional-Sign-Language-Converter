#include <iostream>
#include <fstream>
#include <filesystem>
#include <unordered_set>
#include <map>
#include <nlohmann/json.hpp>

namespace fs = std::filesystem;
using json = nlohmann::json;

int main() {
    std::string base_path = "data";  // path to your data folder
    std::string output_file = "combined_avg_landmarks.json";

    // Allowed words
    std::unordered_set<std::string> allowed_words = {
        "he", "how", "go", "come", "eat", "drink", "help", "know", "give", "father",
        "brother", "baby", "boy", "before", "book", "bed", "bread", "banana", "black",
        "blue", "bad", "angry", "apple", "car", "chair", "cold", "candy", "computer",
        "cousin", "coffee", "day", "different", "door", "after", "good", "girl", "home",
        "house", "hot", "happy", "i"
    };

    json combined;

    for (const auto& entry : fs::directory_iterator(base_path)) {
        if (!entry.is_directory()) continue;

        std::string word = entry.path().filename().string();
        if (allowed_words.find(word) == allowed_words.end()) continue;

        fs::path rotation_file = entry.path() / (word + "_average_landmarks.json");

        if (!fs::exists(rotation_file)) {
            std::cerr << "⚠️ Missing: " << rotation_file << std::endl;
            continue;
        }

        try {
            std::ifstream in(rotation_file);
            json data;
            in >> data;
            combined[word] = data;
        } catch (const std::exception& e) {
            std::cerr << "❌ Error reading " << rotation_file << ": " << e.what() << std::endl;
        }
    }

    try {
        std::ofstream out(output_file);
        out << combined.dump(2);
        std::cout << "✅ Combined rotation file created → " << output_file << std::endl;
    } catch (const std::exception& e) {
        std::cerr << "❌ Error writing output file: " << e.what() << std::endl;
    }

    return 0;
}
