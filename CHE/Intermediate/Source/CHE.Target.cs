using UnrealBuildTool;

public class CHETarget : TargetRules
{
	public CHETarget(TargetInfo Target) : base(Target)
	{
		Type = TargetType.Game;
		ExtraModuleNames.Add("CHE");
	}
}
