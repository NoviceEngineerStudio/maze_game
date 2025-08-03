#ifndef MG_SRC_SCENE_GAME_OBJECT_H
#define MG_SRC_SCENE_GAME_OBJECT_H

namespace mg {
    class GameObject;

    class IComponent {
    public:
        virtual ~IComponent() = default;

    private:
        GameObject* gameobject = nullptr;
    };

    class GameObject {
    public:
        GameObject() = default;

        GameObject(const GameObject&) = delete;
        GameObject(GameObject&&) = delete;

        GameObject& operator=(const GameObject&) = delete;
        GameObject& operator=(GameObject&&) = delete;

        ~GameObject();

        /// @brief Add a component to this Game Object.
        /// @tparam T The component's type.
        /// @tparam ...Args Types of the constructor parameters of type T.
        /// @param ...component_data The constructor parameters of the component.
        template<typename T, typename ...Args>
        void addComponent(Args ...component_data) {
            
        }

        /// @brief Remove a component from this Game Object.
        /// @tparam T The component's type.
        template<typename T>
        void removeComponent() {

        }

        /// @brief Grab a reference to one of the Game Objects components.
        /// @tparam T The component's type.
        /// @return A reference to one of the Game Objects components.
        template<typename T>
        T& getComponent() {

        }

        /// @brief Grab a constant reference to one of the Game Objects components.
        /// @tparam T The component's type.
        /// @return A constant reference to one of the Game Objects components.
        template<typename T>
        const T& getComponent() const {

        }

        /// @brief Determine if this Game Object has a component of type T.
        /// @tparam T The component's type.
        /// @return A boolean showing if this Game Object has a component of type T.
        template<typename T>
        bool hasComponent() const {

        }

    private:
    };
}

#endif