using BenchmarkTools

using Revise
includet("nbabel2.jl")

let data = read_ICs("../data/input16")
    id, mass, pos, vel = data
end

let data = read_ICs("../data/input16")
    id, mass, pos, vel = data
    acc = similar(vel)

    compute_acceleration(pos, mass, acc)
end

let data = read_ICs("../data/input16")
    id, mass, pos, vel = data
    acc = similar(vel)

    compute_acceleration(pos, mass, acc)

    update_positions(pos, vel, acc, 0.1)
end

let data = read_ICs("../data/input16")
    id, mass, pos, vel = data
    acc = similar(vel)

    @btime compute_energy($pos, $vel, $mass)
end

let data = read_ICs("../data/input16")
    id, mass, pos, vel = data
    acc = similar(vel)

    @btime compute_acceleration($pos, $mass, $acc)
end

let data = read_ICs("../data/input16")
    id, mass, pos, vel = data
    acc = similar(vel)

    compute_acceleration(pos, mass, acc)

    @btime update_positions($pos, $vel, $acc, 0.1)
end

let
    @btime NBabel("../data/input16"; show = false)
  # 32.614 ms (470375 allocations: 44.46 MiB)
end

let data = read_ICs("../data/input16")
    id, mass, pos, vel = data
    @btime NBabelCalcs($id, $mass, $pos, $vel)
  # 32.354 ms (470101 allocations: 44.41 MiB)
  # 9.211 ms (5 allocations: 1.05 KiB)
end

let data = read_ICs("../data/input1k")
    id, mass, pos, vel = data
    # NBabelCalcs(id, mass, pos, vel, 0.001)
    @btime NBabelCalcs($id, $mass, $pos, $vel, 0.1)
  # 32.354 ms (470101 allocations: 44.41 MiB)
  # 9.211 ms (5 allocations: 1.05 KiB)
end

########################################
# NBabel
########################################
module OldNBabel

include("nbabel.jl")

# let data = read_ICs("../data/input16")
#     id, mass, pos, vel = data

#     acc = similar(vel)

#     println(compute_acceleration(pos, mass, acc))
# end

# let data = read_ICs("../data/input16")
#     id, mass, pos, vel = data

#     acc = similar(vel)

#     println(compute_energy(pos, vel, mass))
# end

# let data = read_ICs("../data/input16")
#     id, mass, pos, vel = data

#     acc = similar(vel)
#     compute_acceleration(pos, mass, acc)

#     println(update_positions(pos, vel, acc, 0.1))
# end
let
    println(NBabel("../data/input16"; show = false))
end
end # module

########################################
# Profiling
########################################
using ProfileVega
using Profile
Profile.clear()

let data = read_ICs("../data/input1k")
    id, mass, pos, vel = data
    @profview NBabelCalcs(id, mass, pos, vel, 0.1)
    ProfileVega.view()
end



########################################
# Tests
########################################
module Tests
using ReTest
using Main: NBabel, read_ICs, compute_acceleration, compute_energy, update_positions, compute_acceleration2

@testset "All calcs" begin
@testset "calcs validate" begin
    res = NBabel("../data/input16"; show = false)
    
    @test res.Ekin ≈ 1.9107921457919699 atol=1e-4
    @test res.Epot ≈ -0.20118116578813638 atol=1e-5
end

@testset "compute acceleration" begin
    data = read_ICs("../data/input16")
    id, mass, pos, vel = data
    acc = similar(vel)

    res = compute_acceleration(pos, mass, acc)
    @test all(res[1] .≈ (1.45964092973889, 0.2002363627511544, -4.300153496927157))
    @test all(res[16] .≈ (0.5058681955620565, 0.4675207516966996, 0.3369925536658813))
end

@testset "compute energy" begin
    data = read_ICs("../data/input16")
    id, mass, pos, vel = data

    res = compute_energy(pos, vel, mass)
    @test res[1] ≈ 0.25
    @test res[2] ≈ -0.5
end

@testset "update positions" begin
    data = read_ICs("../data/input16")
    id, mass, pos, vel = data
    acc = similar(vel)

    compute_acceleration(pos, mass, acc)

    res = update_positions(pos, vel, acc, 0.1)

    @test all(res[1] .≈ (0.2979190123730081,-0.10370369289709035,-0.294837914359977))
    @test all(res[16] .≈ (-0.6844425306006416,-0.34960613635996524,-0.5958844339746673))
end
end

end # module

Tests.runtests(Tests)
