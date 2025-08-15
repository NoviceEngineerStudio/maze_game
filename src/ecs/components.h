#ifndef MG_SRC_ECS_COMPONENTS_H
#define MG_SRC_ECS_COMPONENTS_H

#include "../core.h"

namespace mg {
    typedef re::u32 ComponentID;

    struct ComponentData {
        ComponentID id = 0;
        re::u32 size = 0;
    };

    template <typename T>
    static ComponentID getComponentID() {
        static ComponentID next_id = 0;
        return next_id++;
    }

    template <typename T>
    static ComponentData getComponentData() {
        return ComponentData {
            .id = getComponentID<T>(),
            .size = sizeof(T),  
        };
    }
}

#endif